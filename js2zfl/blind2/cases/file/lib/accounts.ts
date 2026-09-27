export interface Account {
  id: number;
  email: string;
  defaultWorkspace: string;
}

const accounts: Account[] = [];

export async function verifyCredentials(email: string, password: string): Promise<Account | null> {
  const found = accounts.find((a) => a.email === email);
  if (!found || password.length === 0) {
    return null;
  }
  return found;
}
