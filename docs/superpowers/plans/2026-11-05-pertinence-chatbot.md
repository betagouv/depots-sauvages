# Amélioration Pertinence Chatbot & Sécurisation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Améliorer globalement la pertinence de l'Assistant IA pour les utilisateurs connectés (activation des primo-utilisateurs, suivi des dossiers actifs, RAG multi-tours avec règles contradictoires exactes) tout en garantissant un accès strictement authentifié et une confidentialité Zero-PII.

**Architecture:** 
1. Backend Django : `ChatbotChatView` restreint aux utilisateurs authentifiés, extraction d'un contexte de session strictement anonymisé (`backend/chatbot/context.py`), épurateur anti-PII à la volée (`scrub_pii`), intégration d'une fiche métier détaillée (`guide_suivi_procedure_et_modeles.md`) et RAG multi-tours avec exclusion des FAQ citoyens.
2. Adaptateurs IA : Prise en charge des modèles OpenRouter (`deepseek/deepseek-v4-flash-latest`, `deepseek/deepseek-chat`) et Albert API (`gemma-4-31b-it`, `mistral-small`).
3. Frontend Vue : Splash de connexion ProConnect / démo si anonyme, injection de `currentPath` et détection du profil primo-utilisateur vs dossiers en cours pour afficher des questions d'accueil ciblées.

**Tech Stack:** Python 3.10, Django 4.x, Django REST Framework, Vue 3, Pinia, TypeScript, Vercel AI SDK.

**Spec:** `docs/superpowers/specs/2026-11-05-pertinence-chatbot-design.md`

## Global Constraints
- Aucune PII (Nom, prénom, email, téléphone, adresse postale, plaque, SIRET) ne doit transiter vers les API d'IA.
- Seuls les utilisateurs authentifiés peuvent converser avec l'assistant.
- La compatibilité avec Albert API et OpenRouter doit être assurée.

---

### Task 1: Module de Contexte Anonymisé & Épurateur Anti-PII

**Files:**
- Create: `backend/chatbot/context.py`
- Modify: `backend/chatbot/views.py`
- Test: `backend/chatbot/tests.py`

**Interfaces:**
- Produces: `scrub_pii(text: str) -> str`
- Produces: `build_safe_user_context(user, current_path: str = "") -> Dict[str, Any]`

- [ ] **Step 1: Écrire les tests unitaires pour `scrub_pii` et `build_safe_user_context`**
- [ ] **Step 2: Vérifier l'échec initial des tests**
- [ ] **Step 3: Implémenter `backend/chatbot/context.py`**
- [ ] **Step 4: Mettre à jour `ChatbotChatView` avec `IsAuthenticated` et l'injection du contexte sécurisé**
- [ ] **Step 5: Exécuter les tests et vérifier qu'ils passent**

---

### Task 2: Fiche de Connaissance Métier & Moteur RAG Multi-tours

**Files:**
- Create: `backend/chatbot/knowledge/custom/guide_suivi_procedure_et_modeles.md`
- Modify: `backend/chatbot/retriever.py`
- Test: `backend/chatbot/tests.py`

**Interfaces:**
- Modifies: `KnowledgeRetriever.search(query: str, top_k: int = 3, exclude_public_faq: bool = True) -> List[Dict[str, str]]`

- [ ] **Step 1: Rédiger la fiche de référence `guide_suivi_procedure_et_modeles.md`**
- [ ] **Step 2: Écrire les tests pour la recherche multi-tours et l'exclusion de la FAQ citoyenne**
- [ ] **Step 3: Implémenter le filtrage et les synonymes dans `KnowledgeRetriever`**
- [ ] **Step 4: Exécuter les tests de recherche documentaire**

---

### Task 3: Support Modèles OpenRouter (deepseek-v4-flash-latest) & Directives Système

**Files:**
- Modify: `backend/chatbot/adapters.py`
- Test: `backend/chatbot/tests.py`

- [ ] **Step 1: Mettre à jour `SYSTEM_PROMPT` et la sélection de modèle par défaut dans `adapters.py`**
- [ ] **Step 2: Intégrer l'épurateur anti-PII dans le flux de messages avant l'envoi API**
- [ ] **Step 3: Tester les adaptateurs (Mock, OpenRouter, Albert)**

---

### Task 4: Frontend - Splash ProConnect & Prompts d'Accueil Adaptatifs

**Files:**
- Modify: `frontend/components/AssistantDrawer.vue`

- [ ] **Step 1: Intégrer l'état non-authentifié avec `LoginInvitation` dans le drawer**
- [ ] **Step 2: Adapter les prompts d'accueil selon `proceduresCount == 0` vs `proceduresCount > 0` et le dossier actif**
- [ ] **Step 3: Transmettre le contexte de navigation (`currentPath`, `procedureId`) dans l'appel `useChat`**
- [ ] **Step 4: Vérifier le build frontend et la non-régression**

---

### Task 5: Validation Globale & Tests Réels sur Albert API et OpenRouter

- [ ] **Step 1: Exécuter la suite complète de tests Django**
- [ ] **Step 2: Effectuer un test de validation réel via script sur OpenRouter et Albert API**
- [ ] **Step 3: Vérifier l'absence totale de fuite PII dans les payloads envoyés**
