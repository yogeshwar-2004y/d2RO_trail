import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ObservationReport from '@/components/ObservationReport.vue'

describe('ObservationReport.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    wrapper = mount(ObservationReport)
  })

  it('renders correctly', () => {
    expect(wrapper.find('.observation-report').exists()).toBe(true)
  })

  it('initializes with default observation data', () => {
    expect(wrapper.vm.observationData).toHaveProperty('reportId')
    expect(wrapper.vm.observationData).toHaveProperty('date')
    expect(wrapper.vm.observationData).toHaveProperty('inspector')
    expect(wrapper.vm.observationData).toHaveProperty('project')
  })

  it('initializes with empty observations array', () => {
    expect(Array.isArray(wrapper.vm.observations)).toBe(true)
    expect(wrapper.vm.observations).toHaveLength(0)
  })

  it('adds new observation', async () => {
    const newObservation = {
      category: 'Quality',
      description: 'Test observation',
      severity: 'High',
      status: 'Open'
    }
    
    await wrapper.vm.addObservation(newObservation)
    
    expect(wrapper.vm.observations).toHaveLength(1)
    expect(wrapper.vm.observations[0]).toMatchObject(newObservation)
  })

  it('removes observation by index', async () => {
    // Add some observations first
    await wrapper.setData({
      observations: [
        { id: 1, category: 'Quality', description: 'Obs 1' },
        { id: 2, category: 'Safety', description: 'Obs 2' },
        { id: 3, category: 'Process', description: 'Obs 3' }
      ]
    })
    
    await wrapper.vm.removeObservation(1)
    
    expect(wrapper.vm.observations).toHaveLength(2)
    expect(wrapper.vm.observations[1].id).toBe(3)
  })

  it('updates observation status', async () => {
    await wrapper.setData({
      observations: [
        { id: 1, category: 'Quality', description: 'Test', status: 'Open' }
      ]
    })
    
    await wrapper.vm.updateObservationStatus(0, 'Closed')
    
    expect(wrapper.vm.observations[0].status).toBe('Closed')
  })

  it('validates observation data before adding', async () => {
    const invalidObservation = {
      category: '',
      description: '',
      severity: '',
      status: ''
    }
    
    const result = await wrapper.vm.validateObservation(invalidObservation)
    
    expect(result).toBe(false)
  })

  it('validates complete observation data', async () => {
    const validObservation = {
      category: 'Quality',
      description: 'Valid observation',
      severity: 'Medium',
      status: 'Open'
    }
    
    const result = await wrapper.vm.validateObservation(validObservation)
    
    expect(result).toBe(true)
  })

  it('generates report summary', async () => {
    await wrapper.setData({
      observations: [
        { category: 'Quality', severity: 'High', status: 'Open' },
        { category: 'Safety', severity: 'Medium', status: 'Closed' },
        { category: 'Quality', severity: 'Low', status: 'Open' }
      ]
    })
    
    const summary = await wrapper.vm.generateSummary()
    
    expect(summary).toHaveProperty('total', 3)
    expect(summary).toHaveProperty('open', 2)
    expect(summary).toHaveProperty('closed', 1)
    expect(summary).toHaveProperty('byCategory')
    expect(summary.byCategory['Quality']).toBe(2)
    expect(summary.byCategory['Safety']).toBe(1)
  })

  it('filters observations by category', async () => {
    await wrapper.setData({
      observations: [
        { category: 'Quality', description: 'Quality issue' },
        { category: 'Safety', description: 'Safety concern' },
        { category: 'Quality', description: 'Another quality issue' },
        { category: 'Process', description: 'Process improvement' }
      ]
    })
    
    const qualityObservations = await wrapper.vm.filterByCategory('Quality')
    
    expect(qualityObservations).toHaveLength(2)
    expect(qualityObservations.every(obs => obs.category === 'Quality')).toBe(true)
  })

  it('filters observations by status', async () => {
    await wrapper.setData({
      observations: [
        { status: 'Open', description: 'Open issue 1' },
        { status: 'Closed', description: 'Closed issue' },
        { status: 'Open', description: 'Open issue 2' },
        { status: 'In Progress', description: 'In progress issue' }
      ]
    })
    
    const openObservations = await wrapper.vm.filterByStatus('Open')
    
    expect(openObservations).toHaveLength(2)
    expect(openObservations.every(obs => obs.status === 'Open')).toBe(true)
  })

  it('exports report data', async () => {
    const mockData = {
      reportId: 'RPT001',
      observations: [
        { category: 'Quality', description: 'Test observation' }
      ]
    }
    
    await wrapper.setData({
      observationData: mockData.reportId,
      observations: mockData.observations
    })
    
    const exportData = await wrapper.vm.exportReport()
    
    expect(exportData).toHaveProperty('reportId')
    expect(exportData).toHaveProperty('observations')
    expect(exportData.observations).toEqual(mockData.observations)
  })

  it('saves draft report', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
    
    await wrapper.vm.saveDraft()
    
    expect(consoleSpy).toHaveBeenCalledWith('Draft saved:', expect.any(Object))
    
    consoleSpy.mockRestore()
  })

  it('submits final report', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
    
    await wrapper.setData({
      observations: [
        { category: 'Quality', description: 'Test', status: 'Open' }
      ]
    })
    
    await wrapper.vm.submitReport()
    
    expect(consoleSpy).toHaveBeenCalledWith('Report submitted:', expect.any(Object))
    
    consoleSpy.mockRestore()
  })

  it('handles empty report submission', async () => {
    await wrapper.setData({ observations: [] })
    
    const result = await wrapper.vm.canSubmitReport()
    
    expect(result).toBe(false)
  })

  it('validates report before submission', async () => {
    await wrapper.setData({
      observations: [
        { category: 'Quality', description: 'Valid observation', status: 'Open' }
      ],
      observationData: {
        reportId: 'RPT001',
        inspector: 'John Doe',
        project: 'Test Project'
      }
    })
    
    const result = await wrapper.vm.canSubmitReport()
    
    expect(result).toBe(true)
  })

  it('maintains observation data integrity', () => {
    const observation = {
      id: 1,
      category: 'Quality',
      description: 'Test observation',
      severity: 'High',
      status: 'Open',
      dateCreated: new Date().toISOString()
    }
    
    wrapper.vm.observations.push(observation)
    
    expect(wrapper.vm.observations[0]).toEqual(observation)
    expect(wrapper.vm.observations[0].id).toBe(1)
    expect(wrapper.vm.observations[0].category).toBe('Quality')
  })

  it('calculates observation statistics', async () => {
    await wrapper.setData({
      observations: [
        { severity: 'High', status: 'Open' },
        { severity: 'High', status: 'Closed' },
        { severity: 'Medium', status: 'Open' },
        { severity: 'Low', status: 'Open' }
      ]
    })
    
    const stats = await wrapper.vm.calculateStats()
    
    expect(stats.totalObservations).toBe(4)
    expect(stats.highSeverity).toBe(2)
    expect(stats.openItems).toBe(3)
    expect(stats.completionRate).toBe(25) // 1 closed out of 4 total
  })
})
