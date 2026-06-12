import TodoItem from './TodoItem';

function TodoList({ todos, loadTodos }) {
  return (
    <ul id="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.todo_id}
          todo={todo}
          loadTodos={loadTodos}
        />
      ))}
    </ul>
  );
}

export default TodoList;
