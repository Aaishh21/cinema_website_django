(function(){
    // Support multiple eye-icon toggles across the page.
    // Each .eye-icon should either have a data-target="#inputId" or be placed next to the input inside .password-wrapper.
    const icons = Array.from(document.querySelectorAll('.eye-icon'));
    if(!icons.length) return;

    icons.forEach(icon => {
        // find target input: data-target attribute prefers, otherwise look for nearest input in wrapper
        let targetId = icon.getAttribute('data-target');
        let input = null;
        if(targetId) input = document.getElementById(targetId);
        if(!input){
            // try to find an input sibling inside the same wrapper
            const wrapper = icon.closest('.password-wrapper') || icon.parentElement;
            if(wrapper) input = wrapper.querySelector('input[type="password"], input[type="text"]');
        }
        const closed = icon.querySelector('.icon-closed');
        const open = icon.querySelector('.icon-open');

        function setState(show){
            // show === true means reveal (show text / show the open-eye)
            if(input) input.type = show ? 'text' : 'password';
            if(closed) closed.classList.toggle('hidden', show);
            if(open) open.classList.toggle('hidden', !show);
            icon.setAttribute('aria-pressed', show ? 'true' : 'false');
        }

        // initial state: hidden (closed-eye visible)
        setState(false);

        // click toggles. If we have an input, base toggle on its current type; otherwise base on closed svg visibility.
        icon.addEventListener('click', () => {
            const show = input ? (input.type === 'password') : (closed ? !closed.classList.contains('hidden') : false);
            setState(show);
        });

        icon.addEventListener('keydown', (e) => {
            if(e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar'){
                e.preventDefault();
                const show = input ? (input.type === 'password') : (closed ? !closed.classList.contains('hidden') : false);
                setState(show);
            }
        });
    });
})();

// Profile dropdown toggle
(function(){
    const dropdown = document.getElementById('profileDropdown');
    const btn = document.getElementById('profileBtn');
    if(!dropdown || !btn) return;

    const menu = dropdown.querySelector('.dropdown-menu');

    function openMenu(){
        dropdown.classList.add('open');
        btn.setAttribute('aria-expanded','true');
        // focus first item for keyboard users
        const first = menu.querySelector('[role="menuitem"]');
        if(first) first.focus();
    }

    function closeMenu(){
        dropdown.classList.remove('open');
        btn.setAttribute('aria-expanded','false');
    }

    btn.addEventListener('click', (e)=>{
        e.stopPropagation();
        if(dropdown.classList.contains('open')) closeMenu(); else openMenu();
    });

    // close when clicking outside
    document.addEventListener('click', (e)=>{
        if(!dropdown.contains(e.target)) closeMenu();
    });

    // keyboard: Esc to close
    document.addEventListener('keydown', (e)=>{
        if(e.key === 'Escape' || e.key === 'Esc'){
            if(dropdown.classList.contains('open')){
                closeMenu();
                btn.focus();
            }
        }
    });
})();

// Sidebar tab switching (Profile / Orders)
(function(){
    const sideLinks = Array.from(document.querySelectorAll('.side-link'));
    const profileView = document.querySelector('.panel-profile');
    const ordersView = document.querySelector('.panel-orders');
    const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
    if(!sideLinks.length) return;

    sideLinks.forEach(link => {
        link.addEventListener('click', (e)=>{
            e.preventDefault();
            sideLinks.forEach(l=>l.classList.remove('active'));
            link.classList.add('active');
            // toggle views
            if(link.textContent.trim().toLowerCase().includes('order')){
                if(profileView) profileView.style.display = 'none';
                if(ordersView) ordersView.style.display = 'block';
            } else {
                if(profileView) profileView.style.display = 'block';
                if(ordersView) ordersView.style.display = 'none';
            }
        });
    });

    // orders tab buttons - show/hide lists inside .orders-list
    const ordersList = document.querySelector('.orders-list');
    if(ordersList){
        const lists = Array.from(ordersList.querySelectorAll('[data-list]'));

        function showList(name){
            lists.forEach(l => {
                if(l.getAttribute('data-list') === name){
                    l.style.display = '';
                } else {
                    l.style.display = 'none';
                }
            });
        }

        tabButtons.forEach(btn => {
            btn.addEventListener('click', ()=>{
                tabButtons.forEach(b=>b.classList.remove('active'));
                btn.classList.add('active');
                const tab = btn.getAttribute('data-tab');
                showList(tab);
            });
        });

        // default: ensure active tab shows its list
        const activeTab = tabButtons.find(b => b.classList.contains('active'));
        if(activeTab) showList(activeTab.getAttribute('data-tab'));
    }
})();

document.addEventListener("DOMContentLoaded", () => {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const activeList = document.querySelector(".orders-active");
  const pastList = document.querySelector(".orders-past");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Remove active from all tabs
      tabButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const selected = btn.dataset.tab;

      if (selected === "active") {
        activeList.style.display = "block";
        pastList.style.display = "none";
      } else {
        activeList.style.display = "none";
        pastList.style.display = "block";   // Показать empty state !!!
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
    // Get all edit and save buttons
    const editButtons = document.querySelectorAll('.edit-btn');
    const saveButtons = document.querySelectorAll('.save-btn');
    const profileForm = document.getElementById('profileForm');

    // Add click event to all edit buttons
    editButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const fieldName = this.dataset.field;
        const fieldRow = this.closest('.field-row');
        
        // Hide display text and show input
        const displayText = fieldRow.querySelector('.display-text');
        const inputField = fieldRow.querySelector('.edit-input');
        
        if (displayText) displayText.classList.add('hidden');
        if (inputField) inputField.classList.remove('hidden');
        
        // Hide edit button and show save button
        this.classList.add('hidden');
        fieldRow.querySelector('.save-btn').classList.remove('hidden');
        
        // Focus the input
        if (inputField) inputField.focus();
    });
    });

    // Add click event to all save buttons
    saveButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const fieldName = this.dataset.field;
        const fieldRow = this.closest('.field-row');
        
        // Get the input value
        const inputField = fieldRow.querySelector('.edit-input');
        const displayText = fieldRow.querySelector('.display-text');
        
        if (inputField && displayText) {
        // Update display text with new value
        displayText.textContent = inputField.value;
        
        // Hide input and show display text
        inputField.classList.add('hidden');
        displayText.classList.remove('hidden');
        
        // Hide save button and show edit button
        this.classList.add('hidden');
        fieldRow.querySelector('.edit-btn').classList.remove('hidden');
        
        // Submit the form
        profileForm.submit();
        }
    });
    });

    // Avatar upload functionality
    const avatarInput = document.querySelector('.avatar-input');
    const avatarImg = document.querySelector('.avatar');
    
    if (avatarInput) {
    avatarInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
        const file = this.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Preview the image immediately
            avatarImg.src = e.target.result;
        };
        
        reader.readAsDataURL(file);
        
        // Create FormData and submit via AJAX
        const formData = new FormData();
        formData.append('avatar', file);
        
        // Get CSRF token from form
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken.value);
        }
        
        // Get the form action URL or current URL
        const profileForm = document.getElementById('profileForm');
        const actionUrl = profileForm ? profileForm.action : window.location.href;
        
        fetch(actionUrl, {
            method: 'POST',
            body: formData,
            headers: {
            'X-CSRFToken': csrfToken ? csrfToken.value : '',
            }
        })
        .then(response => response.json())
        .catch(error => {
            console.error('Error uploading avatar:', error);
            // Reload page on error to restore previous avatar
            location.reload();
        });
        }
    });
    }
});