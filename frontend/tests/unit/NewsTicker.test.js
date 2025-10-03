import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import NewsTicker from '@/components/NewsTicker.vue'

// Mock fetch
global.fetch = vi.fn()

describe('NewsTicker.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch.mockClear()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  const createWrapper = (props = {}) => {
    return mount(NewsTicker, {
      props: {
        height: '50px',
        speed: 100,
        backgroundColor: '#2c3e50',
        textColor: '#ffffff',
        showWhenEmpty: true,
        fallbackText: 'Welcome to Aviatrax',
        ...props
      }
    })
  }

  describe('Component Rendering', () => {
    it('renders with default props', () => {
      wrapper = createWrapper()
      expect(wrapper.find('.news-ticker-container').exists()).toBe(true)
      expect(wrapper.find('.news-ticker').exists()).toBe(true)
      expect(wrapper.find('.news-content').exists()).toBe(true)
    })

    it('applies custom height and background color', () => {
      wrapper = createWrapper({
        height: '60px',
        backgroundColor: '#ff0000'
      })
      
      const container = wrapper.find('.news-ticker-container')
      expect(container.attributes('style')).toContain('height: 60px')
      expect(container.attributes('style')).toContain('background-color: rgb(255, 0, 0)')
    })

    it('applies custom text color', () => {
      wrapper = createWrapper({
        textColor: '#00ff00'
      })
      
      const content = wrapper.find('.news-content')
      expect(content.attributes('style')).toContain('color: rgb(0, 255, 0)')
    })
  })

  describe('News Loading', () => {
    it('loads news on mount', async () => {
      const mockNews = [
        { news_text: 'Test news 1' },
        { news_text: 'Test news 2' }
      ]
      
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockNews)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/news')
    })

    it('handles successful news loading', async () => {
      const mockNews = [
        { news_text: 'Breaking news' },
        { news_text: 'Important update' }
      ]
      
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockNews)
      })

      wrapper = createWrapper()
      await wrapper.vm.loadNews()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.news).toEqual(mockNews)
      expect(wrapper.vm.loading).toBe(false)
    })

    it('handles news loading errors gracefully', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.loadNews()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.news).toEqual([])
      expect(wrapper.vm.loading).toBe(false)
    })

    it('prevents multiple simultaneous loading requests', async () => {
      global.fetch.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

      wrapper = createWrapper()
      
      // Start multiple load requests
      const promise1 = wrapper.vm.loadNews()
      const promise2 = wrapper.vm.loadNews()
      
      await Promise.all([promise1, promise2])

      // Should only call fetch once
      expect(global.fetch).toHaveBeenCalledTimes(1)
    })
  })

  describe('Display Logic', () => {
    it('shows fallback text when no news and showWhenEmpty is true', () => {
      wrapper = createWrapper({
        showWhenEmpty: true,
        fallbackText: 'Custom fallback'
      })
      
      wrapper.setData({ news: [] })
      
      expect(wrapper.vm.displayNews).toEqual(['Custom fallback', 'Custom fallback'])
    })

    it('shows empty array when no news and showWhenEmpty is false', () => {
      wrapper = createWrapper({
        showWhenEmpty: false
      })
      
      wrapper.setData({ news: [] })
      
      expect(wrapper.vm.displayNews).toEqual([])
    })

    it('repeats news items for continuous scrolling', () => {
      const mockNews = [
        { news_text: 'News 1' },
        { news_text: 'News 2' }
      ]
      
      wrapper = createWrapper()
      wrapper.setData({ news: mockNews })
      
      const expected = [...mockNews, ...mockNews, ...mockNews]
      expect(wrapper.vm.displayNews).toEqual(expected)
    })

    it('handles string news items', () => {
      wrapper = createWrapper()
      wrapper.setData({ news: ['String news 1', 'String news 2'] })
      
      const newsItems = wrapper.findAll('.news-item')
      expect(newsItems[0].text()).toContain('String news 1')
      expect(newsItems[1].text()).toContain('String news 2')
    })
  })

  describe('Computed Properties', () => {
    it('hasNews returns true when news array has items', () => {
      wrapper = createWrapper()
      wrapper.setData({ news: [{ news_text: 'Test' }] })
      
      expect(wrapper.vm.hasNews).toBe(true)
    })

    it('hasNews returns false when news array is empty', () => {
      wrapper = createWrapper()
      wrapper.setData({ news: [] })
      
      expect(wrapper.vm.hasNews).toBe(false)
    })

    it('animationStyle returns correct CSS properties', () => {
      wrapper = createWrapper()
      
      const style = wrapper.vm.animationStyle
      expect(style.animationDuration).toBe('30s')
      expect(style.animationTimingFunction).toBe('linear')
      expect(style.animationIterationCount).toBe('infinite')
    })
  })

  describe('Component Visibility', () => {
    it('shows component when hasNews is true', () => {
      wrapper = createWrapper()
      wrapper.setData({ news: [{ news_text: 'Test' }] })
      
      expect(wrapper.find('.news-ticker-container').isVisible()).toBe(true)
    })

    it('shows component when showWhenEmpty is true and no news', () => {
      wrapper = createWrapper({
        showWhenEmpty: true
      })
      wrapper.setData({ news: [] })
      
      expect(wrapper.find('.news-ticker-container').isVisible()).toBe(true)
    })

    it('hides component when showWhenEmpty is false and no news', () => {
      wrapper = createWrapper({
        showWhenEmpty: false
      })
      wrapper.setData({ news: [] })
      
      expect(wrapper.find('.news-ticker-container').isVisible()).toBe(false)
    })
  })

  describe('News Items Rendering', () => {
    it('renders news items with correct format', () => {
      const mockNews = [
        { news_text: 'First news item' },
        { news_text: 'Second news item' }
      ]
      
      wrapper = createWrapper()
      wrapper.setData({ news: mockNews })
      
      const newsItems = wrapper.findAll('.news-item')
      expect(newsItems.length).toBeGreaterThan(0)
      expect(newsItems[0].text()).toContain('📰 First news item')
    })

    it('handles empty news text gracefully', () => {
      wrapper = createWrapper()
      wrapper.setData({ news: [{ news_text: '' }] })
      
      const newsItems = wrapper.findAll('.news-item')
      expect(newsItems[0].text()).toContain('📰')
    })
  })

  describe('Auto-refresh Functionality', () => {
    it('sets up interval for news refresh', () => {
      vi.useFakeTimers()
      
      wrapper = createWrapper()
      
      // Fast-forward time to trigger interval
      vi.advanceTimersByTime(30000)
      
      expect(global.fetch).toHaveBeenCalledTimes(2) // Initial call + interval call
      
      vi.useRealTimers()
    })
  })

  describe('Edge Cases', () => {
    it('handles null news response', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(null)
      })

      wrapper = createWrapper()
      await wrapper.vm.loadNews()
      
      expect(wrapper.vm.news).toEqual([])
    })

    it('handles malformed news response', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve('invalid data')
      })

      wrapper = createWrapper()
      await wrapper.vm.loadNews()
      
      expect(wrapper.vm.news).toEqual([])
    })

    it('handles network timeout', async () => {
      global.fetch.mockImplementation(() => 
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Timeout')), 100)
        )
      )

      wrapper = createWrapper()
      await wrapper.vm.loadNews()
      
      expect(wrapper.vm.news).toEqual([])
      expect(wrapper.vm.loading).toBe(false)
    })
  })
})