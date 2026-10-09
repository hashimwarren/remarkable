import { test, expect } from '@playwright/test';

test('sidebar startup, editing, persistence, explicit approval and chat handoff', async ({ page }) => {
  await page.goto('/?app=sidebar');
  const frame = page.frameLocator('#app');
  await frame.getByRole('button', { name: 'New', exact: true }).click();
  await expect(frame.getByLabel('Document ID')).not.toHaveValue('');
  const id = await frame.getByLabel('Document ID').inputValue();
  await frame.getByRole('button', { name: 'Premise', exact: true }).click();
  await frame.getByLabel('View', { exact: true }).selectOption('source');
  await frame.getByLabel('Markdown source', { exact: true }).fill('A confirmed premise.');
  await frame.getByRole('button', { name: 'Save edits', exact: true }).click();
  await expect(frame.getByRole('status')).toHaveText('Saved.');
  await frame.getByRole('button', { name: 'Outline', exact: true }).click();
  await frame.getByLabel('Markdown source', { exact: true }).fill('# Working outline\n\n- Show the mechanism\n- Present evidence');
  await frame.getByRole('button', { name: 'Save edits', exact: true }).click();
  await expect(frame.getByRole('status')).toHaveText('Saved.');
  await frame.getByRole('button', { name: 'Approve outline', exact: true }).click();
  await expect(frame.locator('#approval')).toHaveText('Outline approved');
  await frame.getByRole('button', { name: 'Article', exact: true }).click();
  await frame.getByLabel('Markdown source', { exact: true }).fill('# Human draft\n\nKeep these words.');
  await frame.getByRole('button', { name: 'Ask Remarkable in chat', exact: true }).click();
  await expect(page.locator('#messages')).toContainText(id);
  await frame.getByRole('button', { name: 'Reload saved version', exact: true }).click();
  await expect(frame.getByLabel('Markdown source', { exact: true })).toHaveValue('# Human draft\n\nKeep these words.');
});

test('polling preserves unsaved human edits and reports a conflicting save', async ({ page }) => {
  await page.goto('/');
  const frame = page.frameLocator('#app');
  await expect(frame.getByLabel('Document ID')).not.toHaveValue('');
  await frame.getByLabel('View', { exact: true }).selectOption('source');
  await frame.getByLabel('Markdown source', { exact: true }).fill('Unsaved human text');
  await page.getByRole('button', { name: 'Simulate chat agent update' }).click();
  await expect(frame.getByRole('status')).toContainText('unsaved edits are preserved');
  await expect(frame.getByLabel('Markdown source', { exact: true })).toHaveValue('Unsaved human text');
  await frame.getByRole('button', { name: 'Save edits', exact: true }).click();
  await expect(frame.getByRole('status')).toContainText('Conflict');
});

test('unsupported messaging provides a copyable prompt and rich text remains editable', async ({ page }) => {
  await page.goto('/?noMessages&textOnly&blob');
  const frame = page.frameLocator('#app');
  await expect(frame.getByLabel('Document ID')).not.toHaveValue('');
  await frame.getByRole('textbox', { name: 'Article editor' }).fill('A rich text edit.');
  await frame.getByRole('button', { name: 'Ask Remarkable in chat', exact: true }).click();
  await expect(frame.getByLabel('Message to copy into chat')).toBeVisible();
  await expect(frame.getByLabel('Message to copy into chat')).toHaveValue(/get_writing_guide/);
  await frame.getByRole('button', { name: 'Reload saved version', exact: true }).click();
  await expect(frame.getByRole('textbox', { name: 'Article editor' })).toContainText('A rich text edit.');
});
