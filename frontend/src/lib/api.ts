export type ExpenseInput = {
  date: string;
  description: string;
  amount: number;
};

export type ExpenseDto = {
  id: string;
  date: string;
  description: string;
  amount: number;
  status: "pending" | "approved" | "reimbursed";
  submittedBy: "Mila";
};

// Default to local backend if env is not provided
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers |
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export const api = {
  listExpenses: () => request<ExpenseDto[]>("/api/expenses"),
  addExpense: (body: ExpenseInput) =>
    request<ExpenseDto>("/api/expenses", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  approveExpense: (id: string) =>
    request<ExpenseDto>(`/api/expenses/${id}/approve`, { method: "POST" }),
  reimburse: (amount: number) =>
    request<{ remaining: number }>("/api/reimburse", {
      method: "POST",
      body: JSON.stringify({ amount }),
    }),
};


