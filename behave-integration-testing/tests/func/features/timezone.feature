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

    Examples: <payload>, <status>, <return_code>
      | payload               | field  |
      | {"timezone": "UTC"}   | body   |
      | {"timezone": "Fake"}  | errors |
