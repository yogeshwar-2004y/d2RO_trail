// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

// Custom commands for AVIATRAX application

// Login command
Cypress.Commands.add("loginWithCredentials", (email, password) => {
  cy.request({
    method: "POST",
    url: "http://localhost:5000/api/login",
    body: {
      email: email,
      password: password,
    },
  }).then((response) => {
    expect(response.status).to.eq(200);
    expect(response.body.success).to.be.true;

    // Store user data in localStorage
    window.localStorage.setItem("user", JSON.stringify(response.body.user));
  });
});

// Visit page with authentication
Cypress.Commands.add(
  "visitWithAuth",
  (
    url,
    userCredentials = { email: "test@example.com", password: "password" }
  ) => {
    cy.loginWithCredentials(userCredentials.email, userCredentials.password);
    cy.visit(url);
  }
);

// Wait for element with timeout
Cypress.Commands.add("waitForElement", (selector, timeout = 10000) => {
  cy.get(selector, { timeout });
});

// Upload file command
Cypress.Commands.add(
  "uploadFile",
  (selector, fileName, fileType = "text/plain") => {
    cy.fixture(fileName).then((fileContent) => {
      cy.get(selector).attachFile({
        fileContent: fileContent.toString(),
        fileName: fileName,
        mimeType: fileType,
      });
    });
  }
);
