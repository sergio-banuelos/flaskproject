
Feature:
    Administrar_Citas

Scenario:
    Login into the system
    Given I go to "http://127.0.0.1:5000/appointments/"
    When I fill in field with id "username" with "email@cimat.mx"
    And I fill in field with id "password" with "thepassword"
    And I submit the form

Scenario:
    Create an appoitment
    Given I go to "http://127.0.0.1:5000/appointments/create/"
    When I fill in field with id "title" with "Nueva Cita"
    And I fill in field with id "start" with "2010-11-11 12:00:00"
    And I fill in field with id "end" with "2010-11-11 13:00:00"
    And I fill in field with id "location" with "Av. Universidad"
    And I fill in field with id "description" with "Nueva Cita Agendada"
    And I submit the form


Scenario:
    Edit a given appointment
    Given I go to "http://127.0.0.1:5000/appointments/1/edit"
    When I update the field with id "title" with "Titulo Nuevo"
    And I submit the form
    Then I see that the element with class
    "appointment-detail"
    contains "Titulo Nuevo"


Scenario:
    Delete an appoitment
    Given I go to "http://127.0.0.1:5000/appointments/"
    When I select the appointment with the title "Borrar cita"
    And I do click in the button "appointment-delete-link"
    And I go to "http://127.0.0.1:5000/appointments/"
    Then I see that the element with the class "appointment-detail"
    not contains "Borrar cita"

Scenario:
    Out into the system
    Given I go to "http://127.0.0.1:5000/login/"
    When I select the appointment with the title "Logout"
    And I do click in the button "http://127.0.0.1:5000/login/"
    And I go to "http://127.0.0.1:5000/login/"
    And I submit the form
