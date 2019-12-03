create_mutation = '''
    mutation TODO_CREATE(
        $calendarId: Int!
        $title: String!
        $description: String
        $date: DateTime
        $labelId: Int
    ) {
        createTodo(
            calendarId: $calendarId,
            title: $title,
            description: $description,
            date: $date,
            labelId: $labelId
        ) {
            todo {
                id,
            }
        }
    }
'''

update_mutation = '''
    mutation TODO_UPDATE(
        $todoId: Int!
        $title: String
        $description: String
        $date: DateTime
        $labelId: Int
        $done: Boolean
    ) {
        updateTodo(
            todoId: $todoId,
            title: $title,
            description: $description,
            date: $date,
            labelId: $labelId,
            done: $done
        ) {
            todo {
                title,
                id,
                description,
                date,
                done,
                label {
                    name,
                    id,
                }
            }
        }
    }
'''
