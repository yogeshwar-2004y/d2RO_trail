describe('Dashboard Navigation Flow', () => {
  beforeEach(() => {
    // Mock successful login
    cy.intercept('POST', '**/api/login', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Login successful',
        user: {
          id: 1001,
          name: 'Test User',
          email: 'test@example.com',
          role_id: 1,
          role: 'admin'
        }
      }
    }).as('loginRequest')

    // Visit login page
    cy.visit('/')
    
    // Login
    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    
    cy.wait('@loginRequest')
  })

  it('should navigate to projects dashboard', () => {
    // Mock projects API
    cy.intercept('GET', '**/api/projects', {
      statusCode: 200,
      body: [
        {
          id: 1,
          project_id: 'PROJ001',
          name: 'Test Project 1',
          status: 'active',
          created_date: '2024-01-01'
        }
      ]
    }).as('getProjects')

    // Navigate to projects
    cy.contains('Projects').click()
    
    cy.wait('@getProjects')
    
    // Verify projects dashboard
    cy.url().should('include', '/projects')
    cy.contains('PROJECTS').should('be.visible')
    cy.contains('PROJ001').should('be.visible')
  })

  it('should navigate to LRU dashboard', () => {
    // Mock LRUs API
    cy.intercept('GET', '**/api/lrus', {
      statusCode: 200,
      body: [
        {
          id: 1,
          lru_name: 'LRU001',
          project_id: 'PROJ001',
          status: 'active',
          created_date: '2024-01-01'
        }
      ]
    }).as('getLrus')

    // Navigate to LRUs
    cy.contains('LRU').click()
    
    cy.wait('@getLrus')
    
    // Verify LRU dashboard
    cy.url().should('include', '/lrus')
    cy.contains('LRU DASHBOARD').should('be.visible')
    cy.contains('LRU001').should('be.visible')
  })

  it('should navigate to memos dashboard', () => {
    // Mock memos API
    cy.intercept('GET', '**/api/memos', {
      statusCode: 200,
      body: [
        {
          id: 1,
          memo_id: 'MEMO001',
          title: 'Test Memo 1',
          status: 'draft',
          created_date: '2024-01-01'
        }
      ]
    }).as('getMemos')

    // Navigate to memos
    cy.contains('Memos').click()
    
    cy.wait('@getMemos')
    
    // Verify memos dashboard
    cy.url().should('include', '/memos')
    cy.contains('MEMOS').should('be.visible')
    cy.contains('MEMO001').should('be.visible')
  })

  it('should navigate to reports dashboard', () => {
    // Mock reports API
    cy.intercept('GET', '**/api/reports', {
      statusCode: 200,
      body: [
        {
          id: 1,
          report_id: 'RPT001',
          title: 'Test Report 1',
          type: 'inspection',
          status: 'completed',
          created_date: '2024-01-01'
        }
      ]
    }).as('getReports')

    // Navigate to reports
    cy.contains('Reports').click()
    
    cy.wait('@getReports')
    
    // Verify reports dashboard
    cy.url().should('include', '/reports')
    cy.contains('REPORTS').should('be.visible')
    cy.contains('RPT001').should('be.visible')
  })
})
