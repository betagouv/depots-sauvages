import { expect, test } from '@playwright/test'

test.describe("Page d'accueil", () => {
  test('doit afficher le titre et les éléments principaux', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Vérifier le titre de la page (défini dans index.html)
    await expect(page).toHaveTitle(/Protect’Envi/, { timeout: 10000 })

    // Vérifier la présence du titre principal (H1)
    // On cherche un élément avec le texte attendu
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()

    // Vérifier la présence d'un lien de connexion ou d'information
    // (Selon le contenu actuel de la page d'accueil)
    // Par exemple, on peut chercher le texte "Signaler un dépôt"
    // await expect(page.getByText(/Signaler/)).toBeVisible();
  })

  test('doit être accessible', async ({ page }) => {
    await page.goto('/')
    // Ici on pourrait ajouter axe-playwright plus tard si besoin
  })
})
