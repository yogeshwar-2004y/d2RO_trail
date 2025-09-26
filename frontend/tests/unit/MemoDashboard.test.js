import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import MemoDashboard from '@/components/MemoDashboard.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      currentUserRole: vi.fn(() => 2)
    }
  }
}))

describe('MemoDashboard.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    wrapper = mount(MemoDashboard)
  })

  it('renders correctly', () => {
    expect(wrapper.find('.memo-dashboard').exists()).toBe(true)
    
    const titleElement = wrapper.find('h1')
    if (titleElement.exists()) {
      expect(titleElement.text()).toContain('Memo Dashboard')
    }
  })

  it('initializes with predefined memo statuses', () => {
    const expectedStatuses = [
      'SUCCESSFULLY COMPLETED',
      'DISAPPROVED', 
      'ASSIGNED',
      'COMPLETED WITH OBSERVATIONS',
      'TEST NOT CONDUCTED',
      'NOT ASSIGNED'
    ]
    
    const componentStatuses = wrapper.vm.memoStatuses.map(s => s.name)
    expectedStatuses.forEach(status => {
      expect(componentStatuses).toContain(status)
    })
  })

  it('initializes with sample memo data', () => {
    expect(Array.isArray(wrapper.vm.memos)).toBe(true)
    // Check if memos array exists and has expected structure
    if (wrapper.vm.memos.length > 0) {
      expect(wrapper.vm.memos[0]).toHaveProperty('id')
      expect(wrapper.vm.memos[0]).toHaveProperty('project')
    }
  })

  it('filters memos by project', async () => {
    await wrapper.setData({ activeProjectFilter: 'PROJ001' })
    
    const filtered = wrapper.vm.filteredMemos
    expect(filtered.every(memo => memo.project === 'PROJ001')).toBe(true)
  })

  it('filters memos by status', async () => {
    await wrapper.setData({ activeMemoFilter: 'ASSIGNED' })
    
    const filtered = wrapper.vm.filteredMemos
    expect(filtered.every(memo => memo.status === 'ASSIGNED')).toBe(true)
  })

  it('filters memos by search query', async () => {
    await wrapper.setData({ searchQuery: 'PROJ001' })
    
    const filtered = wrapper.vm.filteredMemos
    expect(filtered.every(memo => memo.project.includes('PROJ001'))).toBe(true)
  })

  it('combines all filters correctly', async () => {
    await wrapper.setData({
      activeProjectFilter: 'PROJ001',
      activeMemoFilter: 'SUCCESSFULLY COMPLETED',
      searchQuery: 'PROJ001'
    })
    
    const filtered = wrapper.vm.filteredMemos
    expect(filtered.every(memo => 
      memo.project === 'PROJ001' && 
      memo.status === 'SUCCESSFULLY COMPLETED'
    )).toBe(true)
  })

  it('toggles project filter visibility', async () => {
    expect(wrapper.vm.showProjectFilter).toBe(false)
    
    await wrapper.vm.toggleProjectFilter()
    expect(wrapper.vm.showProjectFilter).toBe(true)
    
    await wrapper.vm.toggleProjectFilter()
    expect(wrapper.vm.showProjectFilter).toBe(false)
  })

  it('toggles memo filter visibility', async () => {
    expect(wrapper.vm.showMemoFilter).toBe(false)
    
    await wrapper.vm.toggleMemoFilter()
    expect(wrapper.vm.showMemoFilter).toBe(true)
    
    await wrapper.vm.toggleMemoFilter()
    expect(wrapper.vm.showMemoFilter).toBe(false)
  })

  it('sets active project filter', async () => {
    await wrapper.setData({ activeProjectFilter: 'PROJ002' })
    
    expect(wrapper.vm.activeProjectFilter).toBe('PROJ002')
  })

  it('sets active memo filter', async () => {
    await wrapper.setData({ activeMemoFilter: 'ASSIGNED' })
    
    expect(wrapper.vm.activeMemoFilter).toBe('ASSIGNED')
  })

  it('clears project filter', async () => {
    await wrapper.setData({ activeProjectFilter: 'PROJ001' })
    await wrapper.setData({ activeProjectFilter: null })
    
    expect(wrapper.vm.activeProjectFilter).toBe(null)
  })

  it('clears memo filter', async () => {
    await wrapper.setData({ activeMemoFilter: 'ASSIGNED' })
    await wrapper.setData({ activeMemoFilter: null })
    
    expect(wrapper.vm.activeMemoFilter).toBe(null)
  })

  it('calculates unread notifications correctly', () => {
    const unreadCount = wrapper.vm.unreadNotifications
    const expectedUnread = wrapper.vm.notifications.filter(n => !n.isRead).length
    
    expect(unreadCount).toBe(expectedUnread)
  })

  it('handles notification reading', async () => {
    const initialUnread = wrapper.vm.unreadNotifications
    
    // Mark first unread notification as read
    const firstUnread = wrapper.vm.notifications.find(n => !n.isRead)
    if (firstUnread) {
      firstUnread.isRead = true
      await wrapper.vm.$nextTick()
      
      expect(wrapper.vm.unreadNotifications).toBe(initialUnread - 1)
    }
  })

  it('computes user role from store', () => {
    expect(wrapper.vm.currentUserRole).toBe(2)
  })

  it('returns all memos when no filters applied', async () => {
    await wrapper.setData({
      activeProjectFilter: null,
      activeMemoFilter: null,
      searchQuery: ''
    })
    
    expect(wrapper.vm.filteredMemos).toEqual(wrapper.vm.memos)
  })

  it('handles empty search results', async () => {
    await wrapper.setData({ searchQuery: 'NONEXISTENT' })
    
    expect(wrapper.vm.filteredMemos).toHaveLength(0)
  })

  it('maintains notification data integrity', () => {
    wrapper.vm.notifications.forEach(notification => {
      expect(notification).toHaveProperty('id')
      expect(notification).toHaveProperty('project')
      expect(notification).toHaveProperty('status')
      expect(notification).toHaveProperty('isRead')
      expect(typeof notification.isRead).toBe('boolean')
    })
  })
})
