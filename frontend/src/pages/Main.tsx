import { useEffect, useMemo, useState } from "react";
import UserForm from "../components/UserForm";
import {
  createUser,
  deleteUser,
  fetchRandomUser,
  listUsers,
  updateUser,
  extractErrorMessage,
  type User,
} from "../lib/api";

const blankUser: User = {
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  gender: "",
  addresses: [{ street: "", city: "", country: "", timezone: { offset: "", description: "" } }],
} as any;

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [sort, setSort] = useState<string>("first_name");
  const [editing, setEditing] = useState<User | null>(null);
  const [draft, setDraft] = useState<User | null>(null);
  const [status, setStatus] = useState<string>("");
  const [isError, setIsError] = useState<boolean>(false);

  const load = async () => {
    try {
      setIsError(false);
      setStatus("Завантаження користувачів...");
      const data = await listUsers({ sort });
      setUsers(data);
      setStatus(`Завантажено ${data.length} користувачів`);
    } catch (e) {
      setIsError(true);
      setStatus(extractErrorMessage(e));
    }
  };

  useEffect(() => {
    load();
  }, [sort]);

  const current = useMemo<User>(() => {
    if (editing) return editing;
    if (draft) return draft;
    return blankUser;
  }, [editing, draft, users]);

  const handleCreateEmpty = () => {
    setIsError(false);
    setStatus("Створення нового користувача");
    setEditing(null);
    setDraft(blankUser);
  };

  const handleLoadRandom = async () => {
    try {
      setIsError(false);
      setStatus("Завантаження випадкового користувача...");
      const data = await fetchRandomUser();
      // Ensure we treat random user as new (no id)
      const { id, ...rest } = data as any;
      setEditing(null);
      setDraft({ ...(rest as User), id: undefined });
      setStatus("Випадкового користувача завантажено. Ви можете відредагувати та зберегти його в БД.");
    } catch (e) {
      setIsError(true);
      setStatus(extractErrorMessage(e));
    }
  };

  const save = async (u: User) => {
    try {
      setIsError(false);
      if (u.id) {
        setStatus("Збереження змін...");
        await updateUser(u.id, u);
        setStatus("Користувача оновлено");
      } else {
        setStatus("Збереження нового користувача...");
        await createUser(u);
        setStatus("Користувача створено");
      }
      setEditing(null);
      setDraft(null);
      await load();
    } catch (e) {
      setIsError(true);
      setStatus(extractErrorMessage(e));
    }
  };

  const remove = async (id: number) => {
    try {
      setIsError(false);
      setStatus("Видалення користувача...");
      await deleteUser(id);
      setStatus("Користувача видалено");
      await load();
    } catch (e) {
      setIsError(true);
      setStatus(extractErrorMessage(e));
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="page-title">Користувачі</h2>
      <p className="min-h-6">
        {status ? (
          <span className={`badge ${isError ? "badge-error" : "badge-info"}`}>{status}</span>
        ) : (
          <span className="muted">Ще не виконано жодної дії</span>
        )}
      </p>

      <div className="space-y-6">
        <div className="card space-y-4">
          <div className="flex flex-wrap gap-2">
            <button className="btn btn-ghost" type="button" onClick={handleCreateEmpty}>
              Новий користувач
            </button>
            <button className="btn btn-primary" type="button" onClick={handleLoadRandom}>
              Завантажити випадкового
            </button>
          </div>
          <UserForm
            initial={current}
            onSubmit={save}
            submitText={current?.id ? "Оновити" : "Створити"}
          />
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <label className="text-slate-300">Сортувати за:</label>
              <select className="select max-w-xs w-40" value={sort} onChange={(e) => setSort(e.target.value)}>
                <option value="first_name">Іменем</option>
                <option value="last_name">Прізвищем</option>
                <option value="email">Email</option>
              </select>
            </div>
          </div>

          <div className="card max-h-[60vh] overflow-auto">
            {users.length === 0 ? (
              <div className="flex items-center justify-center py-10">
                <span className="muted">
                  {isError
                    ? "Не вдалося завантажити користувачів. Спробуйте ще раз пізніше."
                    : "Користувачів ще немає"}
                </span>
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
                    <button
                      className="btn btn-primary"
                      type="button"
                      onClick={() => {
                        setDraft(null);
                        setEditing(u);
                      }}
                    >
                      Редагувати
                    </button>
                    <button className="btn btn-danger" type="button" onClick={() => remove(u.id!)}>
                      Видалити
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


