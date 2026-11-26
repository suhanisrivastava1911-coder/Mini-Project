/**
 * Admin Dashboard Management JS
 * Handles Officer analytics, Scheme CRUD, user listings, and audit trail.
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Check Admin Auth
  try {
    const authRes = await fetch('/api/admin/me');
    if (!authRes.ok) {
      window.location.href = '/pages/admin_login.html';
      return;
    }
    const adminData = await authRes.json();
    if (!adminData.authenticated) {
      window.location.href = '/pages/admin_login.html';
      return;
    }
    document.getElementById('admin-name').textContent = adminData.admin.username;
    document.getElementById('admin-role-badge').textContent = adminData.admin.role || 'Officer';
  } catch (err) {
    window.location.href = '/pages/admin_login.html';
    return;
  }

  // Logout handler
  document.getElementById('btn-admin-logout').addEventListener('click', async () => {
    await fetch('/api/admin/logout', { method: 'POST' });
    window.location.href = '/pages/admin_login.html';
  });

  // Tab switching
  document.querySelectorAll('.admin-nav-item[data-tab]').forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelectorAll('.admin-nav-item').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.admin-tab-pane').forEach(p => p.classList.add('hidden'));

      tab.classList.add('active');
      const targetPane = document.getElementById(tab.dataset.tab);
      if (targetPane) targetPane.classList.remove('hidden');

      if (tab.dataset.tab === 'tab-schemes') loadAdminSchemes();
      if (tab.dataset.tab === 'tab-users') loadAdminUsers();
      if (tab.dataset.tab === 'tab-audit') loadAdminAudit();
    });
  });

  // Load Initial Overview Stats
  loadAdminStats();

  // Modal logic for adding schemes
  const modal = document.getElementById('modal-add-scheme');
  document.getElementById('btn-add-scheme-modal')?.addEventListener('click', () => {
    modal.classList.remove('hidden');
  });
  document.getElementById('btn-close-modal')?.addEventListener('click', () => {
    modal.classList.add('hidden');
  });
  document.getElementById('btn-cancel-modal')?.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  // Create Scheme Form Submission
  document.getElementById('form-create-scheme')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      scheme_name: document.getElementById('new-scheme-name').value.trim(),
      provider_ministry: document.getElementById('new-scheme-provider').value.trim(),
      scheme_level: document.getElementById('new-scheme-level').value,
      max_benefit_amount: parseFloat(document.getElementById('new-scheme-benefit').value) || 0,
      description: document.getElementById('new-scheme-desc').value.trim(),
      is_demo: document.getElementById('new-scheme-isdemo').checked
    };

    try {
      const res = await fetch('/api/admin/schemes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        modal.classList.add('hidden');
        document.getElementById('form-create-scheme').reset();
        loadAdminSchemes();
        loadAdminStats();
        alert('Scheme created successfully!');
      } else {
        const d = await res.json();
        alert('Error: ' + (d.error || 'Failed to create scheme.'));
      }
    } catch (err) {
      alert('Error creating scheme.');
    }
  });
});

async function loadAdminStats() {
  try {
    const res = await fetch('/api/admin/dashboard/stats');
    if (res.ok) {
      const data = await res.json();
      const s = data.stats || {};
      document.getElementById('admin-total-schemes').textContent = s.total_schemes || 0;
      document.getElementById('admin-total-users').textContent = s.total_users || 0;
      document.getElementById('admin-total-matches').textContent = s.total_matches || 0;
      document.getElementById('admin-total-checklists').textContent = s.total_checklists || 0;

      const breakdown = document.getElementById('stats-category-breakdown');
      if (s.verified_vs_demo) {
        breakdown.innerHTML = `
          <div class="flex-between py-1"><span>Verified Official Schemes:</span> <strong>${s.verified_vs_demo.verified || 0}</strong></div>
          <div class="flex-between py-1"><span>Demonstration Records:</span> <strong>${s.verified_vs_demo.demo || 0}</strong></div>
        `;
      }
    }
  } catch (e) {
    console.error('Error fetching admin stats:', e);
  }
}

async function loadAdminSchemes() {
  const tbody = document.getElementById('schemes-table-body');
  try {
    const res = await fetch('/api/admin/schemes');
    const data = await res.json();
    const schemes = data.schemes || [];

    if (schemes.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="text-center p-3 text-muted">No schemes in master repository.</td></tr>';
      return;
    }

    tbody.innerHTML = schemes.map(s => `
      <tr>
        <td>${s.id}</td>
        <td><strong>${escapeHtml(s.scheme_name)}</strong></td>
        <td><span class="badge badge-light uppercase">${escapeHtml(s.scheme_level || 'central')}</span></td>
        <td>₹${Number(s.max_benefit_amount || 0).toLocaleString('en-IN')}</td>
        <td>${s.is_demo ? '<span class="badge badge-warning">DEMO</span>' : '<span class="badge badge-primary">OFFICIAL</span>'}</td>
        <td>${s.is_active ? '✅ Active' : '❌ Inactive'}</td>
        <td>
          <button class="btn btn-xs btn-danger btn-delete-scheme" data-id="${s.id}">Delete</button>
        </td>
      </tr>
    `).join('');

    // Delete handlers
    tbody.querySelectorAll('.btn-delete-scheme').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        if (!confirm('Are you sure you want to delete this scheme?')) return;
        const sid = e.target.dataset.id;
        await fetch(`/api/admin/schemes/${sid}`, { method: 'DELETE' });
        loadAdminSchemes();
        loadAdminStats();
      });
    });
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-danger text-center">Error loading schemes.</td></tr>';
  }
}

async function loadAdminUsers() {
  const tbody = document.getElementById('users-table-body');
  try {
    const res = await fetch('/api/admin/users');
    const data = await res.json();
    const users = data.users || [];

    if (users.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-center p-3 text-muted">No registered users yet.</td></tr>';
      return;
    }

    tbody.innerHTML = users.map(u => `
      <tr>
        <td>${u.id}</td>
        <td>${escapeHtml(u.name || '')}</td>
        <td>${escapeHtml(u.email || '')}</td>
        <td>${escapeHtml(u.preferred_language || 'en')}</td>
        <td>${u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}</td>
      </tr>
    `).join('');
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-danger text-center">Error loading users.</td></tr>';
  }
}

async function loadAdminAudit() {
  const tbody = document.getElementById('audit-table-body');
  try {
    const res = await fetch('/api/admin/audit-logs');
    const data = await res.json();
    const logs = data.logs || [];

    if (logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="text-center p-3 text-muted">No audit logs recorded yet.</td></tr>';
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr>
        <td>${l.created_at ? new Date(l.created_at).toLocaleString() : 'N/A'}</td>
        <td>${escapeHtml(l.admin_username || 'system')}</td>
        <td>${escapeHtml(l.action || '')}</td>
        <td>${escapeHtml(l.target_id || '-')}</td>
        <td>${escapeHtml(l.ip_address || '127.0.0.1')}</td>
      </tr>
    `).join('');
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-danger text-center">Error loading audit logs.</td></tr>';
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[m]));
}
