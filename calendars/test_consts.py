calendars_get = '''
    {
        calendars {
            id
        }
    }
'''

mutation_create = '''
    mutation CALENDAR_CREATE(
        $name: String!
    ) {
        createCalendar(name: $name) {
            calendar {
                name,
                id,
            }
        }
    }
'''