#!/usr/bin/env node

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Paths
const reportsDir = path.join(__dirname, '../reports/frontend')
const coverageDir = path.join(reportsDir, 'coverage')
const cypressDir = path.join(reportsDir, 'cypress')

// Ensure reports directory exists
if (!fs.existsSync(reportsDir)) {
  fs.mkdirSync(reportsDir, { recursive: true })
}

// Generate comprehensive test report
function generateTestReport() {
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      unitTests: getUnitTestSummary(),
      e2eTests: getE2ETestSummary(),
      coverage: getCoverageSummary()
    },
    details: {
      unitTestResults: getUnitTestResults(),
      e2eTestResults: getE2ETestResults(),
      coverageDetails: getCoverageDetails()
    }
  }

  // Write JSON report
  fs.writeFileSync(
    path.join(reportsDir, 'test-report.json'),
    JSON.stringify(report, null, 2)
  )

  // Generate HTML report
  const htmlReport = generateHTMLReport(report)
  fs.writeFileSync(
    path.join(reportsDir, 'test-report.html'),
    htmlReport
  )

  console.log('✅ Test reports generated successfully!')
  console.log(`📊 Coverage report: ${path.join(coverageDir, 'index.html')}`)
  console.log(`🧪 E2E report: ${path.join(cypressDir, 'cypress-report.html')}`)
  console.log(`📋 Summary report: ${path.join(reportsDir, 'test-report.html')}`)
}

function getUnitTestSummary() {
  try {
    const coverageSummary = JSON.parse(
      fs.readFileSync(path.join(coverageDir, 'coverage-summary.json'), 'utf8')
    )
    
    return {
      total: coverageSummary.total.lines.total,
      covered: coverageSummary.total.lines.covered,
      percentage: coverageSummary.total.lines.pct,
      statements: coverageSummary.total.statements.pct,
      branches: coverageSummary.total.branches.pct,
      functions: coverageSummary.total.functions.pct
    }
  } catch (error) {
    return { error: 'Coverage data not available' }
  }
}

function getE2ETestSummary() {
  try {
    const cypressReport = JSON.parse(
      fs.readFileSync(path.join(cypressDir, 'cypress-report.json'), 'utf8')
    )
    
    return {
      total: cypressReport.stats.tests,
      passed: cypressReport.stats.passes,
      failed: cypressReport.stats.failures,
      skipped: cypressReport.stats.pending,
      duration: cypressReport.stats.duration
    }
  } catch (error) {
    return { error: 'E2E test data not available' }
  }
}

function getCoverageSummary() {
  try {
    const coverageSummary = JSON.parse(
      fs.readFileSync(path.join(coverageDir, 'coverage-summary.json'), 'utf8')
    )
    
    return {
      lines: coverageSummary.total.lines,
      statements: coverageSummary.total.statements,
      branches: coverageSummary.total.branches,
      functions: coverageSummary.total.functions
    }
  } catch (error) {
    return { error: 'Coverage summary not available' }
  }
}

function getUnitTestResults() {
  try {
    const junitReport = fs.readFileSync(path.join(reportsDir, 'junit.xml'), 'utf8')
    return { junit: junitReport }
  } catch (error) {
    return { error: 'Unit test results not available' }
  }
}

function getE2ETestResults() {
  try {
    const cypressReport = JSON.parse(
      fs.readFileSync(path.join(cypressDir, 'cypress-report.json'), 'utf8')
    )
    return cypressReport
  } catch (error) {
    return { error: 'E2E test results not available' }
  }
}

function getCoverageDetails() {
  try {
    const coverageSummary = JSON.parse(
      fs.readFileSync(path.join(coverageDir, 'coverage-summary.json'), 'utf8')
    )
    return coverageSummary
  } catch (error) {
    return { error: 'Coverage details not available' }
  }
}

function generateHTMLReport(report) {
  return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aviatrax Test Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #007bff;
        }
        .summary-card h3 {
            margin: 0 0 15px 0;
            color: #333;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
        }
        .metric-value {
            font-weight: bold;
            color: #007bff;
        }
        .coverage-bar {
            background: #e9ecef;
            border-radius: 4px;
            height: 20px;
            margin: 10px 0;
            overflow: hidden;
        }
        .coverage-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }
        .test-results {
            margin-top: 30px;
        }
        .test-section {
            margin-bottom: 30px;
        }
        .test-section h3 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .status-passed { color: #28a745; }
        .status-failed { color: #dc3545; }
        .status-skipped { color: #ffc107; }
        .timestamp {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Aviatrax Test Report</h1>
            <p>Comprehensive testing results for frontend application</p>
        </div>
        
        <div class="content">
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>📊 Coverage Summary</h3>
                    ${report.summary.coverage.error ? 
                      `<p>${report.summary.coverage.error}</p>` :
                      `
                      <div class="metric">
                          <span>Lines:</span>
                          <span class="metric-value">${report.summary.coverage.lines.pct}%</span>
                      </div>
                      <div class="coverage-bar">
                          <div class="coverage-fill" style="width: ${report.summary.coverage.lines.pct}%"></div>
                      </div>
                      <div class="metric">
                          <span>Statements:</span>
                          <span class="metric-value">${report.summary.coverage.statements.pct}%</span>
                      </div>
                      <div class="metric">
                          <span>Branches:</span>
                          <span class="metric-value">${report.summary.coverage.branches.pct}%</span>
                      </div>
                      <div class="metric">
                          <span>Functions:</span>
                          <span class="metric-value">${report.summary.coverage.functions.pct}%</span>
                      </div>
                      `
                    }
                </div>
                
                <div class="summary-card">
                    <h3>🧪 Unit Tests</h3>
                    ${report.summary.unitTests.error ? 
                      `<p>${report.summary.unitTests.error}</p>` :
                      `
                      <div class="metric">
                          <span>Total Lines:</span>
                          <span class="metric-value">${report.summary.unitTests.total}</span>
                      </div>
                      <div class="metric">
                          <span>Covered:</span>
                          <span class="metric-value">${report.summary.unitTests.covered}</span>
                      </div>
                      <div class="metric">
                          <span>Coverage:</span>
                          <span class="metric-value">${report.summary.unitTests.percentage}%</span>
                      </div>
                      `
                    }
                </div>
                
                <div class="summary-card">
                    <h3>🎭 E2E Tests</h3>
                    ${report.summary.e2eTests.error ? 
                      `<p>${report.summary.e2eTests.error}</p>` :
                      `
                      <div class="metric">
                          <span>Total Tests:</span>
                          <span class="metric-value">${report.summary.e2eTests.total}</span>
                      </div>
                      <div class="metric">
                          <span>Passed:</span>
                          <span class="metric-value status-passed">${report.summary.e2eTests.passed}</span>
                      </div>
                      <div class="metric">
                          <span>Failed:</span>
                          <span class="metric-value status-failed">${report.summary.e2eTests.failed}</span>
                      </div>
                      <div class="metric">
                          <span>Duration:</span>
                          <span class="metric-value">${Math.round(report.summary.e2eTests.duration / 1000)}s</span>
                      </div>
                      `
                    }
                </div>
            </div>
            
            <div class="test-results">
                <div class="test-section">
                    <h3>📋 Test Execution Summary</h3>
                    <p>This report was generated on ${new Date(report.timestamp).toLocaleString()}</p>
                    <p>All tests have been executed using Vitest for unit testing and Cypress for E2E testing.</p>
                </div>
            </div>
        </div>
        
        <div class="timestamp">
            Generated on ${new Date(report.timestamp).toLocaleString()}
        </div>
    </div>
</body>
</html>
  `
}

// Run the report generation
generateTestReport()
