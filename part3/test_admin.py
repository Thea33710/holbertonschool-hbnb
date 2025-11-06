#!/usr/bin/env python3
"""
Script de test des droits administrateur pour HBnB
Usage: python test_admin_rights.py
"""

import requests
import json
from typing import Optional, Dict, Any
from colorama import init, Fore, Style
import time

# Initialiser colorama pour les couleurs
init(autoreset=True)

# Configuration
BASE_URL = "http://127.0.0.1:5000/api/v1"
ADMIN_EMAIL = "admin@hbnb.com"
ADMIN_PASSWORD = "admin123"

# Variables globales pour stocker les tokens et IDs
admin_token: Optional[str] = None
user_token: Optional[str] = None
created_ids: Dict[str, str] = {}

def print_test(test_name: str):
    """Affiche le nom du test en cours"""
    print(f"\n{'='*60}")
    print(f"{Fore.CYAN}🧪 TEST: {test_name}{Style.RESET_ALL}")
    print('='*60)

def print_success(message: str):
    """Affiche un message de succès"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Affiche un message d'erreur"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Affiche un avertissement"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Affiche une information"""
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

def make_request(method: str, endpoint: str, data: Optional[Dict] = None, 
                 token: Optional[str] = None, expected_status: int = 200) -> tuple:
    """
    Effectue une requête HTTP et vérifie le statut
    
    Returns:
        tuple: (success: bool, response: requests.Response)
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print_error(f"Méthode HTTP non supportée: {method}")
            return False, None
        
        print_info(f"{method} {endpoint} → Status {response.status_code}")
        
        # Afficher la réponse si elle contient du JSON
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response: {response.text}")
        
        success = response.status_code == expected_status
        if success:
            print_success(f"Statut attendu {expected_status} ✓")
        else:
            print_error(f"Statut attendu {expected_status}, reçu {response.status_code}")
        
        return success, response
    
    except requests.exceptions.ConnectionError:
        print_error("❌ Impossible de se connecter au serveur!")
        print_warning("Vérifiez que votre serveur Flask tourne sur http://127.0.0.1:5000")
        return False, None
    except Exception as e:
        print_error(f"Erreur lors de la requête: {str(e)}")
        return False, None

def test_0_create_admin():
    """Test 0: Créer l'administrateur (si nécessaire)"""
    print_test("0. Créer l'administrateur")
    
    print_info("Tentative de création de l'admin...")
    data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "first_name": "Admin",
        "last_name": "User"
    }
    
    # Essayer de créer l'admin (peut échouer si déjà existant)
    success, response = make_request("POST", "/users/", data, expected_status=201)
    
    if not success and response and response.status_code == 400:
        print_warning("L'admin existe déjà (c'est OK)")
        return True
    
    if success and response:
        admin_id = response.json().get('id')
        print_success(f"Admin créé avec ID: {admin_id}")
        print_warning("⚠️  IMPORTANT: Vous devez manuellement définir is_admin=True en base de données!")
        print_warning("   Ou utilisez une des méthodes décrites dans la documentation.")
        return True
    
    return False

def test_1_login_admin():
    """Test 1: Se connecter en tant qu'admin"""
    global admin_token
    
    print_test("1. Connexion administrateur")
    
    data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    success, response = make_request("POST", "/auth/login", data)
    
    if success and response:
        try:
            admin_token = response.json().get('access_token')
            if admin_token:
                print_success(f"Token admin récupéré: {admin_token[:30]}...")
                created_ids['admin_token'] = admin_token
                return True
            else:
                print_error("Pas de token dans la réponse")
        except:
            print_error("Impossible de parser la réponse JSON")
    
    return False

def test_2_create_amenity_without_token():
    """Test 2.1: Créer un amenity SANS token (doit échouer)"""
    print_test("2.1. Créer amenity sans token (doit échouer)")
    
    data = {"name": "Swimming Pool"}
    
    # On s'attend à un 401 ou 403
    success, response = make_request("POST", "/amenities/", data, 
                                     expected_status=401)
    
    if not success and response and response.status_code in [401, 403]:
        print_success("Accès refusé comme attendu ✓")
        return True
    
    return success

def test_3_create_amenity_with_admin():
    """Test 2.2: Créer un amenity AVEC token admin"""
    print_test("2.2. Créer amenity avec token admin")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    data = {"name": "Swimming Pool"}
    
    success, response = make_request("POST", "/amenities/", data, 
                                     token=admin_token, expected_status=201)
    
    if success and response:
        try:
            amenity_id = response.json().get('id')
            created_ids['amenity_id'] = amenity_id
            print_success(f"Amenity créé avec ID: {amenity_id}")
            return True
        except:
            print_error("Impossible de récupérer l'ID de l'amenity")
    
    return False

def test_4_update_amenity():
    """Test 2.3: Modifier l'amenity avec token admin"""
    print_test("2.3. Modifier amenity avec token admin")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    if 'amenity_id' not in created_ids:
        print_error("Pas d'amenity ID disponible")
        return False
    
    amenity_id = created_ids['amenity_id']
    data = {"name": "Heated Swimming Pool"}
    
    success, response = make_request("PUT", f"/amenities/{amenity_id}", 
                                     data, token=admin_token)
    
    return success

def test_5_create_normal_user():
    """Test 3.1: Créer un utilisateur normal"""
    print_test("3.1. Créer un utilisateur normal")
    
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "user11@test.com",
        "password": "password123"
    }
    
    success, response = make_request("POST", "/users/", data, expected_status=201)
    
    if success and response:
        try:
            user_id = response.json().get('id')
            created_ids['user1_id'] = user_id
            print_success(f"User créé avec ID: {user_id}")
            return True
        except:
            print_error("Impossible de récupérer l'ID du user")
    
    return False

def test_6_login_normal_user():
    """Test 3.2: Se connecter en tant qu'utilisateur normal"""
    global user_token
    
    print_test("3.2. Connexion utilisateur normal")
    
    data = {
        "email": "user11@test.com",
        "password": "password123"
    }
    
    success, response = make_request("POST", "/auth/login", data)
    
    if success and response:
        try:
            user_token = response.json().get('access_token')
            created_ids['user_token'] = user_token
            print_success(f"Token user récupéré: {user_token[:30]}...")
            return True
        except:
            print_error("Impossible de parser la réponse JSON")
    
    return False

def test_7_admin_create_user():
    """Test 3.3: Admin crée un nouvel utilisateur"""
    print_test("3.3. Admin crée un nouvel utilisateur")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "newuser1@hbnb.com",
        "password": "password123"
    }
    
    success, response = make_request("POST", "/users/", data, 
                                     token=admin_token, expected_status=201)
    
    if success and response:
        try:
            user_id = response.json().get('id')
            created_ids['user2_id'] = user_id
            print_success(f"User créé par admin avec ID: {user_id}")
            return True
        except:
            print_error("Impossible de récupérer l'ID du user")
    
    return False

def test_8_admin_modify_other_user():
    """Test 3.4: Admin modifie un autre utilisateur"""
    print_test("3.4. Admin modifie un autre utilisateur")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    if 'user1_id' not in created_ids:
        print_error("Pas de user ID disponible")
        return False
    
    user_id = created_ids['user1_id']
    data = {
        "email": "updated@hbnb.com",
        "first_name": "John Updated"
    }
    
    success, response = make_request("PUT", f"/users/{user_id}", 
                                     data, token=admin_token)
    
    return success

def test_9_user_modify_other_user():
    """Test 3.5: User normal essaie de modifier un autre user (doit échouer)"""
    print_test("3.5. User normal essaie de modifier autre user (doit échouer)")
    
    if not user_token:
        print_error("Pas de token user disponible")
        return False
    
    if 'user2_id' not in created_ids:
        print_warning("Pas de user2 disponible, skip ce test")
        return True
    
    user_id = created_ids['user2_id']
    data = {"email": "hacked@hbnb.com"}
    
    success, response = make_request("PUT", f"/users/{user_id}", 
                                     data, token=user_token, expected_status=403)
    
    if not success and response and response.status_code == 403:
        print_success("Modification refusée comme attendu ✓")
        return True
    
    return False

def test_10_user_create_place():
    """Test 4.1: User normal crée un place"""
    print_test("4.1. User normal crée un place")
    
    if not user_token:
        print_error("Pas de token user disponible")
        return False
    
    data = {
        "title": "Beautiful Apartment",
        "description": "A nice place to stay",
        "price": 100,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    
    success, response = make_request("POST", "/", data, 
                                     token=user_token, expected_status=201)
    
    if success and response:
        try:
            place_id = response.json().get('id')
            created_ids['place_id'] = place_id
            print_success(f"Place créé avec ID: {place_id}")
            return True
        except:
            print_error("Impossible de récupérer l'ID du place")
    
    return False

def test_11_admin_modify_user_place():
    """Test 4.2: Admin modifie le place d'un user (bypass ownership)"""
    print_test("4.2. Admin modifie le place d'un user (bypass ownership)")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    if 'place_id' not in created_ids:
        print_error("Pas de place ID disponible")
        return False
    
    place_id = created_ids['place_id']
    data = {
        "title": "Admin Updated Title",
        "price": 150
    }
    
    success, response = make_request("PUT", f"/{place_id}", 
                                     data, token=admin_token)
    
    if success:
        print_success("Admin a pu modifier le place d'un autre user ✓")
    
    return success

def test_12_admin_delete_user_place():
    """Test 4.3: Admin supprime le place d'un user"""
    print_test("4.3. Admin supprime le place d'un user")
    
    if not admin_token:
        print_error("Pas de token admin disponible")
        return False
    
    if 'place_id' not in created_ids:
        print_error("Pas de place ID disponible")
        return False
    
    place_id = created_ids['place_id']
    
    success, response = make_request("DELETE", f"/places/{place_id}", 
                                     token=admin_token)
    
    if success:
        print_success("Admin a pu supprimer le place d'un autre user ✓")
    
    return success

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"🚀 DÉBUT DES TESTS ADMIN HBNB")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    tests = [
        ("Création admin (si nécessaire)", test_0_create_admin),
        ("Connexion admin", test_1_login_admin),
        ("Amenity sans token (échec attendu)", test_2_create_amenity_without_token),
        ("Amenity avec admin", test_3_create_amenity_with_admin),
        ("Modifier amenity", test_4_update_amenity),
        ("Créer user normal", test_5_create_normal_user),
        ("Connexion user normal", test_6_login_normal_user),
        ("Admin crée user", test_7_admin_create_user),
        ("Admin modifie user", test_8_admin_modify_other_user),
        ("User modifie autre user (échec)", test_9_user_modify_other_user),
        ("User crée place", test_10_user_create_place),
        ("Admin modifie place user", test_11_admin_modify_user_place),
        ("Admin supprime place user", test_12_admin_delete_user_place),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(0.5)  # Petite pause entre les tests
        except Exception as e:
            print_error(f"Exception dans le test: {str(e)}")
            results.append((test_name, False))
    
    # Résumé final
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"📊 RÉSUMÉ DES TESTS")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ PASS" if result else f"{Fore.RED}❌ FAIL"
        print(f"{status}{Style.RESET_ALL} - {test_name}")
    
    print(f"\n{Fore.CYAN}Score: {passed}/{total} tests réussis{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}🎉 TOUS LES TESTS SONT PASSÉS !{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Certains tests ont échoué. Vérifiez votre implémentation.{Style.RESET_ALL}\n")
    
    # Afficher les IDs créés
    if created_ids:
        print(f"\n{Fore.BLUE}📋 IDs créés pendant les tests:{Style.RESET_ALL}")
        for key, value in created_ids.items():
            if 'token' in key:
                print(f"  {key}: {value[:30]}...")
            else:
                print(f"  {key}: {value}")

if __name__ == "__main__":
    print(f"\n{Fore.CYAN}Avant de lancer les tests:{Style.RESET_ALL}")
    print("1. Assurez-vous que votre serveur Flask tourne sur http://127.0.0.1:5000")
    print("2. Vous devez avoir un admin avec:")
    print(f"   - Email: {ADMIN_EMAIL}")
    print(f"   - Password: {ADMIN_PASSWORD}")
    print(f"   - is_admin: True (en base de données)")
    print("\nAppuyez sur Entrée pour continuer ou Ctrl+C pour annuler...")
    
    try:
        input()
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests annulés par l'utilisateur.{Style.RESET_ALL}\n")
