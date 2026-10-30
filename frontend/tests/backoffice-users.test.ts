import { flushPromises, mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import UsersTab from '../components/backoffice/UsersTab.vue'
import { useBackofficeStore } from '../stores/backoffice'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    query: {},
    params: {},
    meta: { tab: 'users' },
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}))

describe('UsersTab.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('affiche la liste des utilisateurs et permet de filtrer sur zéro procédure', async () => {
    const store = useBackofficeStore()
    store.users = [
      {
        id: 1,
        email: 'jean@example.com',
        first_name: 'Jean',
        last_name: 'Dupont',
        is_staff: false,
        is_active: true,
        date_joined: '2026-01-15T10:00:00Z',
        last_login: '2026-03-01T14:00:00Z',
        procedures_count: 3,
        has_proconnect: true,
        proconnect_profile: {
          id: 10,
          siret: '12345678900012',
          siren: '123456789',
          organization_label: 'Mairie de Test',
          roles: ['agent_public'],
          sub: 'sub-1',
          created: '2026-01-15T10:00:00Z',
          modified: '2026-01-15T10:00:00Z',
        },
      },
      {
        id: 2,
        email: 'claire@example.com',
        first_name: 'Claire',
        last_name: 'Martin',
        is_staff: true,
        is_active: true,
        date_joined: '2026-02-10T08:30:00Z',
        last_login: null,
        procedures_count: 0,
        has_proconnect: false,
        proconnect_profile: null,
      },
    ]
    store.totalUsersCount = 2

    // Mock fetchUsers so it doesn't override our mock store state
    store.fetchUsers = vi.fn().mockResolvedValue(undefined)

    const wrapper = mount(UsersTab, {
      global: {
        stubs: {
          DsfrPagination: true,
        },
      },
    })

    await flushPromises()

    // Both users should be rendered
    expect(wrapper.text()).toContain('jean@example.com')
    expect(wrapper.text()).toContain('claire@example.com')
    expect(wrapper.text()).toContain('12345678900012')
    expect(wrapper.text()).toContain('Mairie de Test')
    expect(wrapper.text()).toContain('0 procédure')

    // Filter by zero procedures triggers store.fetchUsers with appropriate params
    const selectProcedures = wrapper.find('#filter-procedures-count')
    await selectProcedures.setValue('Non')
    await flushPromises()

    expect(store.fetchUsers).toHaveBeenCalledWith(
      expect.objectContaining({
        has_procedures: 'Non',
      })
    )

    // Filter by proconnect triggers store.fetchUsers
    await selectProcedures.setValue('Tous')
    const selectProconnect = wrapper.find('#filter-proconnect')
    await selectProconnect.setValue('Oui')
    await flushPromises()

    expect(store.fetchUsers).toHaveBeenCalledWith(
      expect.objectContaining({
        has_proconnect: 'Oui',
      })
    )

    // Search filter triggers store.fetchUsers
    await selectProconnect.setValue('Tous')
    const searchInput = wrapper.find('#user-search-input')
    await searchInput.setValue('Mairie')
    await flushPromises()

    expect(store.fetchUsers).toHaveBeenCalledWith(
      expect.objectContaining({
        search: 'Mairie',
      })
    )
  })
})
