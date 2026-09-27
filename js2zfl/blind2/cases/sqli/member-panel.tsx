import * as React from 'react';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function loadMember(email: string) {
  'use server';
  return prisma.$queryRawUnsafe(
    `SELECT id, name, tier FROM members WHERE email = '${email}'`
  );
}

export default async function MemberPanel({ email }: { email: string }) {
  const rows: any[] = (await loadMember(email)) as any[];
  return (
    <section className="member-panel">
      <h2>Member</h2>
      <ul>
        {rows.map((r) => (
          <li key={r.id}>{r.name}</li>
        ))}
      </ul>
    </section>
  );
}
