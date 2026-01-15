Feature: Authentication
    As a first-time loan applicant
    I want to verify my phone number with OTP
    So that I can access the loan application

    Scenario: Successful login with valid OTP
        Given I am on the application homepage
        When I click start application
        And I enter phone number "+254719000000"
        And I click request OTP
        And I enter OTP "0000"
        And I click verify
        Then I should see the personal details page