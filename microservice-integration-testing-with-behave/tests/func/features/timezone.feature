Feature: The timezone service works

  Scenario Outline: The server returns the expected status
      Given the flask server is ready
       When the "<payload>" is posted
       Then the status is "<status>"
       Then the return code is "<return_code>"

    Examples: <payload>, <status>, <return_code>
      | payload              | status   | return_code  |
      | {"timezone": "UTC"}  | OK       | 200          |
      | {"timezone": "Fake"} | Error    | 417          |
      | {}                   | Error    | 417          |

  Scenario Outline: The server response contains the expected field
      Given the flask server is ready
       When the "<payload>" is posted
       Then the response contains "status"
        And the response contains "<field>"

    Examples: <payload>, <field>
      | payload               | field  |
      | {"timezone": "UTC"}   | body   |
      | {"timezone": "Fake"}  | errors |

  Scenario Outline: The server returns a valid timestamp
      Given the flask server is ready
       When the "<payload>" is posted
       Then the response contains a valid timestamp

    Examples: <payload>
      | payload                                                 |
      | {"timezone": "UTC", "format": "yyyy-MM-dd hh:mm:ss tt"} |
      | {"timezone": "UTC", "format": "MM/dd/yyyy HH:mm"}       |

  # No examples needed here, since it's the same every time. So we use the
  # "Scenario" keyword rather than "Scenario Outline"
  Scenario: The server can give help
      Given the flask server is ready
       Then the user can ask for help
        And the status is "OK"
        And help is given
