const state = {
  accounts: [],
  movements: []
};

const money = new Intl.NumberFormat('es-CL', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

// Carga desde la API las cuentas persistidas en SQLite para poblar la interfaz.
async function loadAccounts() {
  const response = await fetch('/api/cuentas');
  state.accounts = await response.json();
  renderAccounts();
  renderAccountOptions();
}

// Agrupa por Activo, Pasivo y Patrimonio; dentro separa corriente/no corriente.
function groupAccounts() {
  const groups = {
    Activo: { Corriente: [], 'No corriente': [] },
    Pasivo: { Corriente: [], 'No corriente': [] },
    Patrimonio: { 'No aplica': [] }
  };

  state.accounts.forEach((account) => {
    groups[account.tipo_cuenta][account.corriente_no_corriente].push(account);
  });

  return groups;
}

// Dentro de cada bloque se vuelve a agrupar por la clasificación contable requerida.
function groupByClassification(accounts) {
  return accounts.reduce((result, account) => {
    if (!result[account.clasificacion]) {
      result[account.clasificacion] = [];
    }
    result[account.clasificacion].push(account);
    return result;
  }, {});
}

function getIncreaseSide(accountType) {
  return accountType === 'Activo' ? 'Debe' : 'Haber';
}

function renderAccounts() {
  const container = document.querySelector('#accounts');
  const groups = groupAccounts();

  container.innerHTML = Object.entries(groups).map(([type, sections]) => `
    <article class="group">
      <h3>${type}</h3>
      ${Object.entries(sections).map(([section, accounts]) => `
        <h4>${section}</h4>
        ${Object.entries(groupByClassification(accounts)).map(([classification, classifiedAccounts]) => `
          <div class="classification-block">
            <p class="classification-title">Clasificación: ${classification}</p>
            <ul class="account-list">
              ${classifiedAccounts.map((account) => `
                <li>
                  <strong>${account.nombre}</strong>
                  <span class="account-code">${account.codigo} · Aumenta por el ${getIncreaseSide(account.tipo_cuenta)}</span>
                </li>
              `).join('')}
            </ul>
          </div>
        `).join('')}
      `).join('')}
    </article>
  `).join('');
}

function renderAccountOptions() {
  const select = document.querySelector('#account-select');
  select.innerHTML = state.accounts.map((account) => (
    `<option value="${account.id}">${account.codigo} - ${account.nombre} (${account.tipo_cuenta})</option>`
  )).join('');
  renderSelectedAccountRule();
}

function renderSelectedAccountRule() {
  const selectedId = Number(document.querySelector('#account-select').value);
  const account = state.accounts.find((item) => item.id === selectedId);
  const rule = document.querySelector('#account-rule');

  if (!account) {
    rule.textContent = '';
    return;
  }

  rule.textContent = `${account.tipo_cuenta}: aumenta por el ${getIncreaseSide(account.tipo_cuenta)}.`;
}

// Suma automáticamente los importes del Debe y Haber cada vez que cambia el asiento.
function renderMovements() {
  const body = document.querySelector('#entry-body');
  body.innerHTML = state.movements.map((movement) => `
    <tr>
      <td>${movement.account.nombre}</td>
      <td>${money.format(movement.debit)}</td>
      <td>${money.format(movement.credit)}</td>
    </tr>
  `).join('');

  const totalDebit = state.movements.reduce((sum, movement) => sum + movement.debit, 0);
  const totalCredit = state.movements.reduce((sum, movement) => sum + movement.credit, 0);
  document.querySelector('#total-debit').textContent = money.format(totalDebit);
  document.querySelector('#total-credit').textContent = money.format(totalCredit);
  renderValidationMessage(totalDebit, totalCredit);
}

// Valida la regla básica: un asiento solo es correcto cuando Debe y Haber son iguales.
function renderValidationMessage(totalDebit, totalCredit) {
  const message = document.querySelector('#balance-message');
  message.className = 'message neutral';

  if (state.movements.length === 0) {
    message.textContent = 'Ingrese movimientos para validar el asiento.';
    return;
  }

  if (Math.abs(totalDebit - totalCredit) < 0.01) {
    message.className = 'message valid';
    message.textContent = 'Asiento balanceado';
  } else {
    message.className = 'message invalid';
    message.textContent = 'Error: el asiento contable no está balanceado';
  }
}

function handleEntrySubmit(event) {
  event.preventDefault();
  const selectedId = Number(document.querySelector('#account-select').value);
  const debit = Number(document.querySelector('#debit-input').value || 0);
  const credit = Number(document.querySelector('#credit-input').value || 0);
  const account = state.accounts.find((item) => item.id === selectedId);

  state.movements.push({ account, debit, credit });
  event.target.reset();
  document.querySelector('#debit-input').value = 0;
  document.querySelector('#credit-input').value = 0;
  renderMovements();
}

document.querySelector('#entry-form').addEventListener('submit', handleEntrySubmit);
document.querySelector('#account-select').addEventListener('change', renderSelectedAccountRule);
loadAccounts();
