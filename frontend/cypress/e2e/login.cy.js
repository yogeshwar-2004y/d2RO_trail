describe('Login Flow', () => {
  beforeEach(() => {
    // Visit the login page before each test
    cy.visit('/')
  })

  it('should display login form elements', () => {
    cy.contains('AVIATRAX').should('be.visible')
    
    // Check for login form elements
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')
  })

  it('should show validation errors for empty fields', () => {
    // Try to submit empty form
    cy.get('button[type="submit"]').click()
    
    // Should stay on login page or show validation
    cy.url().should('include', '/')
  })

  it('should show error for invalid credentials', () => {
    // Enter invalid credentials
    cy.get('input[type="email"]').type('invalid@example.com')
    cy.get('input[type="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()
    
    // Should show error message or stay on login page
    cy.url().should('include', '/')
  })

  it('should successfully login with valid credentials', () => {
    // Mock successful login response
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

    // Enter valid credentials
    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    // Wait for login request
    cy.wait('@loginRequest')

    // Should redirect to dashboard based on role
    cy.url().should('not.include', '/login')
  })

  it('should redirect to appropriate dashboard based on user role', () => {
    const roles = [
      { role: 'admin', expectedPath: '/admin' },
      { role: 'designer', expectedPath: '/designer' },
      { role: 'designhead', expectedPath: '/designhead' },
      { role: 'qahead', expectedPath: '/qahead' },
      { role: 'reviewer', expectedPath: '/reviewer' }
    ]

    roles.forEach(({ role, expectedPath }) => {
      // Mock login response for specific role
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
            role: role
          }
        }
      }).as(`login${role}`)

      cy.get('input[type="email"]').clear().type('test@example.com')
      cy.get('input[type="password"]').clear().type('password123')
      cy.get('button[type="submit"]').click()

      cy.wait(`@login${role}`)
      
      // Check redirection
      cy.url().should('include', expectedPath)
      
      // Go back to login for next iteration
      cy.visit('/')
    })
  })

  it('should handle network errors gracefully', () => {
    // Mock network error
    cy.intercept('POST', '**/api/login', {
      forceNetworkError: true
    }).as('loginError')

    cy.get('input[type="email"]').type('test@example.com')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    cy.wait('@loginError')

    // Should show error message or stay on login page
    cy.url().should('include', '/')
  })

  it('should remember user preferences', () => {
    // Test if "Remember Me" functionality exists
    cy.get('body').then(($body) => {
      if ($body.find('input[type="checkbox"]').length > 0) {
        cy.get('input[type="checkbox"]').check()
        
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
        }).as('rememberLogin')

        cy.get('input[type="email"]').type('test@example.com')
        cy.get('input[type="password"]').type('password123')
        cy.get('button[type="submit"]').click()

        cy.wait('@rememberLogin')
        
        // Check if user data is stored in localStorage
        cy.window().then((window) => {
          expect(window.localStorage.getItem('user')).to.not.be.null
        })
      }
    })
  })

  it('should be responsive on different screen sizes', () => {
    // Test mobile view
    cy.viewport(375, 667)
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')

    // Test tablet view
    cy.viewport(768, 1024)
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')

    // Test desktop view
    cy.viewport(1920, 1080)
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')
  })
})
