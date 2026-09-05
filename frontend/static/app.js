let tg = window.Telegram.WebApp;

tg.expand();
tg.MainButton.hide();

let currentStep = 1;
const totalSteps = 6;

document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/options', {
        headers: {
            'Bypass-Tunnel-Reminder': 'true',
            'ngrok-skip-browser-warning': 'true'
        }
    })
        .then(response => response.json())
        .then(data => {
            const branchSelect = document.getElementById('filial-select');
            const posSelect = document.getElementById('lavozim-select');
            
            if(branchSelect) {
                branchSelect.innerHTML = '<option value="" disabled selected>Tanlang</option>';
                data.branches.forEach(b => {
                    const opt = document.createElement('option');
                    opt.value = b;
                    opt.textContent = b;
                    branchSelect.appendChild(opt);
                });
            }
            
            if(posSelect) {
                posSelect.innerHTML = '<option value="" disabled selected>Tanlang</option>';
                data.positions.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p;
                    opt.textContent = p;
                    posSelect.appendChild(opt);
                });
            }
        })
        .catch(err => console.error("Error loading options:", err));
});

const nextBtn = document.getElementById('next-btn');
const backBtn = document.getElementById('back-btn');
const submitBtn = document.getElementById('submit-btn');

// File inputs text update
const fileInputs = document.querySelectorAll('.file-input');
fileInputs.forEach(input => {
    input.addEventListener('change', function(e) {
        let fileName = e.target.value.split('\\').pop();
        if(fileName) {
            e.target.previousElementSibling.innerText = fileName;
            e.target.parentElement.classList.add('is-active');
        } else {
            e.target.previousElementSibling.innerText = 'Fayl yuklang';
            e.target.parentElement.classList.remove('is-active');
        }
    });
});

function updateSteps() {
    // Hide all steps
    document.querySelectorAll('.step-content').forEach(step => {
        step.classList.remove('active');
    });
    document.querySelectorAll('.step-indicator').forEach(ind => {
        ind.classList.remove('active');
    });
    
    // Show current step
    document.getElementById(`step-${currentStep}`).classList.add('active');
    document.getElementById(`ind-${currentStep}`).classList.add('active');
    
    // Manage buttons
    if (currentStep === 1) {
        backBtn.style.display = 'none';
    } else {
        backBtn.style.display = 'block';
    }
    
    if (currentStep === totalSteps) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'block';
    } else {
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    }
    
    window.scrollTo(0, 0);
}

// Navigation Events
nextBtn.addEventListener('click', () => {
    const currentStepEl = document.getElementById(`step-${currentStep}`);
    const inputs = currentStepEl.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value) {
            input.style.borderColor = '#EF4444';
            isValid = false;
        } else {
            input.style.borderColor = '#E2E8F0';
        }
    });

    // Check radio buttons if required
    const radios = currentStepEl.querySelectorAll('input[type="radio"][required]');
    if (radios.length > 0) {
        let radioNames = [...new Set(Array.from(radios).map(r => r.name))];
        radioNames.forEach(name => {
            let checked = currentStepEl.querySelector(`input[name="${name}"]:checked`);
            if (!checked) {
                isValid = false;
            }
        });
    }
    
    if (!isValid) {
        tg.showAlert("Iltimos, barcha majburiy maydonlarni to'ldiring (*).");
        return;
    }
    
    if (currentStep < totalSteps) {
        currentStep++;
        updateSteps();
    }
});

backBtn.addEventListener('click', () => {
    if (currentStep > 1) {
        currentStep--;
        updateSteps();
    }
});

// Dynamic List Logics
let listData = {
    children: [],
    family: [],
    education: [],
    languages: [],
    software: [],
    experience: []
};

function renderList(listId, dataArray, dataKey) {
    const listEl = document.getElementById(listId);
    const emptyState = document.getElementById(`${dataKey}-empty`);
    
    listEl.innerHTML = '';
    
    if(dataArray.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    dataArray.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'item';
        div.innerHTML = `
            <span>${item}</span>
            <button type="button" class="btn-remove" onclick="removeItem('${dataKey}', ${index}, '${listId}')">O'chirish</button>
        `;
        listEl.appendChild(div);
    });
}

window.removeItem = function(dataKey, index, listId) {
    listData[dataKey].splice(index, 1);
    renderList(listId, listData[dataKey], dataKey);
};

window.addChild = function() {
    let childInfo = window.prompt("Farzand ismini va tug'ilgan yilini kiriting:");
    if(childInfo && childInfo.trim() !== '') {
        listData.children.push(childInfo);
        renderList('children-list', listData.children, 'children');
    }
};

window.addFamily = function() {
    let familyInfo = window.prompt("Oila a'zosining ismi va qarindoshligi (Masalan: Aliyev Vali, Ota):");
    if(familyInfo && familyInfo.trim() !== '') {
        listData.family.push(familyInfo);
        renderList('family-list', listData.family, 'family');
    }
};

window.addEducation = function() {
    let eduInfo = window.prompt("O'qish joyi nomi va mutaxassisligi:");
    if(eduInfo && eduInfo.trim() !== '') {
        listData.education.push(eduInfo);
        renderList('education-list', listData.education, 'education');
    }
};

window.addLanguage = function() {
    let langInfo = window.prompt("Til va bilish darajasi (Masalan: Rus tili, 80%):");
    if(langInfo && langInfo.trim() !== '') {
        listData.languages.push(langInfo);
        renderList('language-list', listData.languages, 'languages');
    }
};

window.addSoftware = function() {
    let softInfo = window.prompt("Dastur nomi va darajasi (Masalan: Excel, O'rta):");
    if(softInfo && softInfo.trim() !== '') {
        listData.software.push(softInfo);
        renderList('software-list', listData.software, 'software');
    }
};

window.addExperience = function() {
    let expInfo = window.prompt("Ish joyi nomi va qancha ishlagansiz:");
    if(expInfo && expInfo.trim() !== '') {
        listData.experience.push(expInfo);
        renderList('experience-list', listData.experience, 'experience');
    }
};

// Form Submission
const form = document.getElementById('anketa-form');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const currentStepEl = document.getElementById(`step-6`);
    const inputs = currentStepEl.querySelectorAll('input[type="file"][required]');
    let isValid = true;
    inputs.forEach(input => {
        if (!input.files || input.files.length === 0) {
            input.parentElement.style.borderColor = '#EF4444';
            isValid = false;
        } else {
            input.parentElement.style.borderColor = '#6366F1';
        }
    });
    
    if (!isValid) {
        tg.showAlert("Iltimos, rasm va hujjatni yuklang.");
        return;
    }
    
    const formData = new FormData(form);
    
    formData.append('user_id', tg.initDataUnsafe?.user?.id || 0);
    formData.append('username', tg.initDataUnsafe?.user?.username || "");
    formData.append('initData', tg.initData || "");
    
    formData.append('dynamic_lists', JSON.stringify(listData));
    
    submitBtn.innerHTML = "Yuborilmoqda...";
    submitBtn.disabled = true;
    
    fetch('/submit_form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            tg.showAlert("Anketa muvaffaqiyatli qabul qilindi!");
            tg.close();
        } else {
            tg.showAlert("Xatolik yuz berdi: " + result.message);
            submitBtn.innerHTML = "✅ Yuborish";
            submitBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        tg.showAlert("Xatolik yuz berdi, qayta urinib ko'ring.");
        submitBtn.innerHTML = "✅ Yuborish";
        submitBtn.disabled = false;
    });
});
