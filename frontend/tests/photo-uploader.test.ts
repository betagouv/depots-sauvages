import PhotoUploader from '@/components/forms/constatation/PhotoUploader.vue'
import { flushPromises, mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('PhotoUploader.vue', () => {
  it('affiche un avertissement DsfrAlert quand on dépasse la limite maximale de photos', async () => {
    const wrapper = mount(PhotoUploader, {
      props: {
        modelValue: [
          'photo1',
          'photo2',
          'photo3',
          'photo4',
          'photo5',
          'photo6',
          'photo7',
          'photo8',
          'photo9',
          'photo10',
        ],
        maxPhotos: 10,
      },
    })
    const dropzone = wrapper.find('.dropzone-container')
    const file = new File(['content'], 'test.png', { type: 'image/png' })
    await dropzone.trigger('drop', {
      dataTransfer: { files: [file] },
    })
    await flushPromises()
    const alert = wrapper.find('.fr-alert')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('Vous avez atteint le nombre maximal de 10 photos')
  })

  it('tronque et avertit dans DsfrAlert quand les fichiers dépassent les slots restants', async () => {
    const wrapper = mount(PhotoUploader, {
      props: {
        modelValue: [
          'photo1',
          'photo2',
          'photo3',
          'photo4',
          'photo5',
          'photo6',
          'photo7',
          'photo8',
          'photo9',
        ],
        maxPhotos: 10,
      },
    })
    const dropzone = wrapper.find('.dropzone-container')
    const file1 = new File(['1'], 'p1.png', { type: 'image/png' })
    const file2 = new File(['2'], 'p2.png', { type: 'image/png' })
    await dropzone.trigger('drop', {
      dataTransfer: { files: [file1, file2] },
    })
    await flushPromises()
    const alert = wrapper.find('.fr-alert')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain(
      'Seules les 1 première(s) photo(s) ont été ajoutées pour ne pas dépasser la limite de 10 photos.'
    )
  })

  it('affiche un message d’erreur quand un fichier dépasse la taille maximale autorisée', async () => {
    const wrapper = mount(PhotoUploader, {
      props: {
        modelValue: [],
        maxFileSizeMb: 1,
      },
    })
    const dropzone = wrapper.find('.dropzone-container')
    const bigFile = new File([new Uint8Array(2 * 1024 * 1024)], 'trop-lourd.jpg', {
      type: 'image/jpeg',
    })
    await dropzone.trigger('drop', {
      dataTransfer: { files: [bigFile] },
    })
    await flushPromises()
    const alert = wrapper.find('.fr-alert')
    expect(alert.exists()).toBe(true)
    expect(alert.classes()).toContain('fr-alert--error')
    expect(alert.text()).toContain('trop-lourd.jpg')
  })
})
