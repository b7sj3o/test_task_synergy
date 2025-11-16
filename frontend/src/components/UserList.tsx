import type { User } from "../interfaces/user";

type Props = {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (id: number) => void;
  emptyText?: string;
};

export default function UserList({ users, onEdit, onDelete, emptyText = "Користувачів ще немає" }: Props) {
  return (
    <div className="card max-h-[60vh] overflow-auto">
      {(!users || users.length === 0) ? (
        <div className="flex items-center justify-center py-10">
          <span className="muted">{emptyText}</span>
        </div>
      ) : (
        users.map((u) => (
          <div
            key={u.id}
            className="flex items-center justify-between border-b border-white/10 py-3 last:border-0 hover:bg-white/5"
          >
            <div className="truncate">
              <strong>
                {u.first_name} {u.last_name}
              </strong>{" "}
              <span className="muted">{u.email}</span>
            </div>
            <div className="flex gap-2">
              <button className="btn btn-primary" type="button" onClick={() => onEdit(u)}>
                Редагувати
              </button>
              <button className="btn btn-danger" type="button" onClick={() => onDelete(u.id!)}>
                Видалити
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}


