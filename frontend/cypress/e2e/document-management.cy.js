describe('Document Management Flow', () => {
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
          role_id: 2,
          role: 'qahead'
        }
      }
    }).as('loginRequest')

    // Visit login page and login
    cy.visit('/')
    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    
    cy.wait('@loginRequest')
  })

  it('should upload and view documents', () => {
    // Mock document upload API
    cy.intercept('POST', '**/api/documents/upload', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Document uploaded successfully',
        document_id: 'DOC001'
      }
    }).as('uploadDocument')

    // Mock document list API
    cy.intercept('GET', '**/api/documents', {
      statusCode: 200,
      body: [
        {
          id: 1,
          document_id: 'DOC001',
          filename: 'test-document.pdf',
          project_id: 'PROJ001',
          status: 'uploaded',
          created_date: '2024-01-01'
        }
      ]
    }).as('getDocuments')

    // Navigate to documents
    cy.contains('Documents').click()
    cy.wait('@getDocuments')

    // Upload a document
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test-document.pdf')
    cy.get('button').contains('Upload').click()
    
    cy.wait('@uploadDocument')
    
    // Verify upload success
    cy.contains('Document uploaded successfully').should('be.visible')
  })

  it('should assign reviewer to document', () => {
    // Mock document details API
    cy.intercept('GET', '**/api/documents/DOC001', {
      statusCode: 200,
      body: {
        id: 1,
        document_id: 'DOC001',
        filename: 'test-document.pdf',
        project_id: 'PROJ001',
        status: 'uploaded',
        assigned_reviewer: null
      }
    }).as('getDocumentDetails')

    // Mock assign reviewer API
    cy.intercept('POST', '**/api/documents/DOC001/assign-reviewer', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Reviewer assigned successfully'
      }
    }).as('assignReviewer')

    // Navigate to document details
    cy.visit('/documents/DOC001')
    cy.wait('@getDocumentDetails')

    // Assign reviewer
    cy.get('button').contains('Assign Reviewer').click()
    cy.get('select').select('reviewer@example.com')
    cy.get('button').contains('Assign').click()
    
    cy.wait('@assignReviewer')
    
    // Verify assignment success
    cy.contains('Reviewer assigned successfully').should('be.visible')
  })

  it('should view document in viewer', () => {
    // Mock document viewer API
    cy.intercept('GET', '**/api/documents/DOC001/view', {
      statusCode: 200,
      body: {
        success: true,
        document_url: '/api/documents/DOC001/file',
        document_type: 'pdf'
      }
    }).as('getDocumentView')

    // Navigate to document viewer
    cy.visit('/documents/DOC001/view')
    cy.wait('@getDocumentView')

    // Verify document viewer loads
    cy.get('.document-viewer').should('be.visible')
    cy.get('.pdf-viewer').should('be.visible')
  })

  it('should add observations to document', () => {
    // Mock observations API
    cy.intercept('POST', '**/api/documents/DOC001/observations', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Observation added successfully',
        observation_id: 'OBS001'
      }
    }).as('addObservation')

    // Navigate to document with observations
    cy.visit('/documents/DOC001/observations')

    // Add observation
    cy.get('textarea').type('This is a test observation')
    cy.get('select').select('Critical')
    cy.get('button').contains('Add Observation').click()
    
    cy.wait('@addObservation')
    
    // Verify observation added
    cy.contains('Observation added successfully').should('be.visible')
    cy.contains('This is a test observation').should('be.visible')
  })
})
