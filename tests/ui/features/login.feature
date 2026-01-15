Feature: Authentication
    As a first-time loan applicant
    I want to verify my phone number with OTP
    So that I can access the loan application


    @smoke
    Scenario: User can log in with valid phone number and OTP
        Given I am on the application homepage
        When I click start application
        And I enter a new phone number
        And I click send OTP
        And I enter OTP "0000"
        And I click verify
        Then I should see the personal details page


    Scenario: User cannot log in with invalid phone number
        Given I am on the application homepage
        When I click start application
        And I enter phone number "0"
        And I click send OTP
        Then I should see the error message "Invalid phone number format"


    Scenario: User cannot log in with empty phone number
        Given I am on the application homepage
        When I click start application
        And I enter phone number " "
        And I click send OTP
        Then I should see the error message "Invalid phone number format"


    Scenario: User cannot log in with invalid OTP
        Given I am on the application homepage
        When I click start application
        And I enter phone number "+254719000000"
        And I click send OTP
        And I enter OTP "1234"
        And I click verify
        Then I should see the error message "Invalid OTP"


    Scenario: User can navigate back from OTP screen
        Given I am on the application homepage
        When I click start application
        And I enter phone number "+256700000000"
        And I click send OTP
        And I click back button
        Then I should see the phone input screen