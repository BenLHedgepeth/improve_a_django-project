# Improve a Django Project

**Objective:** *To refactor a project that was written by another author.*

**Summary:** 
*Upon completion of this project, the following concepts and features were added to make the project more coherent.*

  - Testing
      - Namespaced tests according to what was being tested `test_views, test_forms, test_models`

  - Authentication 
      - User Creation
      - User Login

  - Forms
      - Overiding model field definitions
      - Custom field validators
      - Overide form's `clean()` method
      - Custom field error messages
      - Overiding default form field widgets
      
  - Models
    - Added constraints to fields that call for uniqueness
    - Passed arguments to model fields
    - Defined `get_absolute_url()` for model instances

  - Views
    - Refactored Python code into Django syntax
    - Added `login_required` functionality to limit access to logged in users

  - Templates
    - Refactored templates
      - Established parent/child templates
      - Customized form template rendering
      
