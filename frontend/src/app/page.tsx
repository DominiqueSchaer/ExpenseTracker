"use client";
import { useEffect, useMemo, useState } from "react";
import { api, type ExpenseDto, type ExpenseInput } from "@/lib/api";

export default function Home() {
  const [expenses, setExpenses] = useState<ExpenseDto[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    api
      .listExpenses()
      .then((data: ExpenseDto[]) => {
        if (mounted) setExpenses(data);
      })
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : String(err))
      )
      .finally(() => setLoading(false));
    return () => {
      mounted = false;
    };
  }, []);

  const total = useMemo(
    () => expenses.reduce((sum, e) => sum + e.amount, 0),
    [expenses]
  );
  const pending = useMemo(
    () =>
      expenses
        .filter((e) => e.status === "pending")
        .reduce((sum, e) => sum + e.amount, 0),
    [expenses]
  );

  return (
    <div className="flex flex-col gap-6">
      {error && (
        <div className="rounded-md border border-red-300 bg-red-50 text-red-800 px-4 py-2">
          {error}
        </div>
      )}
      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-md border border-black/10 dark:border-white/15 p-4">
          <div className="text-sm text-black/60 dark:text-white/60">Total</div>
          <div className="text-2xl font-semibold">CHF {total.toFixed(2)}</div>
        </div>
        <div className="rounded-md border border-black/10 dark:border-white/15 p-4">
          <div className="text-sm text-black/60 dark:text-white/60">Pending</div>
          <div className="text-2xl font-semibold">CHF {pending.toFixed(2)}</div>
        </div>
        <div className="rounded-md border border-black/10 dark:border-white/15 p-4">
          <div className="text-sm text-black/60 dark:text-white/60">Approved</div>
          <div className="text-2xl font-semibold">
            CHF {(total - pending).toFixed(2)}
          </div>
        </div>
      </section>

      <section className="rounded-md border border-black/10 dark:border-white/15">
        <div className="px-4 py-3 border-b border-black/10 dark:border-white/15 font-medium">
          Expenses
        </div>
        <div className="divide-y divide-black/10 dark:divide-white/15">
          {loading && (
            <div className="px-4 py-3 text-sm text-black/70 dark:text-white/70">
              Loading...
            </div>
          )}
          {expenses.map((e) => (
            <div key={e.id} className="px-4 py-3 grid grid-cols-6 gap-2 items-center">
              <div className="col-span-2 text-sm">{e.description}</div>
              <div className="text-sm text-black/70 dark:text-white/70">
                {e.date}
              </div>
              <div className="text-right font-medium">CHF {e.amount.toFixed(2)}</div>
              <div>
                <span
                  className={
                    "inline-block text-xs px-2 py-1 rounded-full " +
                    (e.status === "pending"
                      ? "bg-yellow-100 text-yellow-800"
                      : e.status === "approved"
                      ? "bg-green-100 text-green-800"
                      : "bg-blue-100 text-blue-800")
                  }
                >
                  {e.status}
                </span>
              </div>
              <div className="text-right">
                <button
                  className="text-sm px-3 py-1 rounded border border-black/10 dark:border-white/20 hover:bg-black/5 dark:hover:bg-white/10 disabled:opacity-60"
                  onClick={async () => {
                    try {
                      const updated = await api.approveExpense(e.id);
                      setExpenses((prev) =>
                        prev.map((x) => (x.id === e.id ? updated : x))
                      );
                    } catch (err: unknown) {
                      setError(
                        err instanceof Error ? err.message : "Failed to approve"
                      );
                    }
                  }}
                  disabled={e.status !== "pending"}
                >
                  Approve
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-md border border-black/10 dark:border-white/15 p-4">
        <h2 className="font-medium mb-3">Add new expense</h2>
        <AddExpenseForm
          onAdded={(exp) => setExpenses((prev) => [exp, ...prev])}
          onError={(msg) => setError(msg)}
        />
      </section>
    </div>
  );
}

function AddExpenseForm({
  onAdded,
  onError,
}: {
  onAdded: (exp: ExpenseDto) => void;
  onError: (message: string) => void;
}) {
  const [form, setForm] = useState<ExpenseInput>({
    date: new Date().toISOString().slice(0, 10),
    description: "",
    amount: 0,
  });
  const [submitting, setSubmitting] = useState(false);

  return (
    <form
      className="grid grid-cols-1 sm:grid-cols-5 gap-3"
      onSubmit={async (e) => {
        e.preventDefault();
        setSubmitting(true);
        try {
          const created = await api.addExpense(form);
          onAdded(created);
          setForm({ date: form.date, description: "", amount: 0 });
        } catch (err: unknown) {
          onError(
            err instanceof Error ? err.message : "Failed to add expense"
          );
        } finally {
          setSubmitting(false);
        }
      }}
    >
      <input
        type="date"
        className="border border-black/10 dark:border-white/20 rounded px-3 py-2 bg-transparent"
        value={form.date}
        onChange={(e) =>
          setForm((prev: ExpenseInput) => ({ ...prev, date: e.target.value }))
        }
      />
      <input
        type="text"
        placeholder="Description"
        className="border border-black/10 dark:border-white/20 rounded px-3 py-2 bg-transparent"
        value={form.description}
        onChange={(e) =>
          setForm((prev: ExpenseInput) => ({
            ...prev,
            description: e.target.value,
          }))
        }
      />
      <input
        type="number"
        step="0.05"
        min="0"
        placeholder="Amount (CHF)"
        className="border border-black/10 dark:border-white/20 rounded px-3 py-2 bg-transparent"
        value={form.amount}
        onChange={(e) =>
          setForm((prev: ExpenseInput) => ({
            ...prev,
            amount: Number(e.target.value),
          }))
        }
      />
      <div className="flex items-center text-sm text-black/60 dark:text-white/60">
        Status set on server
      </div>
      <button
        type="submit"
        disabled={submitting}
        className="rounded px-3 py-2 bg-foreground text-background hover:opacity-90 disabled:opacity-60"
      >
        {submitting ? "Adding..." : "Add"}
      </button>
    </form>
  );
}
