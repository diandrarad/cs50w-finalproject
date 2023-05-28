const countryCurrencySymbols = {
  GB: '£', // British Pound
  US: '$', // US Dollar
  AT: '€', // Euro
  AU: '$', // Australian Dollar
  BE: '€', // Euro
  BR: 'R$', // Brazilian Real
  CA: '$', // Canadian Dollar
  CH: 'CHF', // Swiss Franc
  DE: '€', // Euro
  ES: '€', // Euro
  FR: '€', // Euro
  IN: '₹', // Indian Rupee
  IT: '€', // Euro
  MX: '$', // Mexican Peso
  NL: '€', // Euro
  NZ: '$', // New Zealand Dollar
  PL: 'zł', // Polish Złoty
  RU: '₽', // Russian Ruble
  SG: '$', // Singapore Dollar
  ZA: 'R' // South African Rand
};

document.addEventListener('DOMContentLoaded', function() {
    const selectedCountryElement = document.getElementById('selectedCountry');
    const selectedCountry = selectedCountryElement.textContent; // Get the selected country value
    const salaryCurrency = document.querySelectorAll('.salary-currency');
    salaryCurrency.forEach(currencySymbols => {
      currencySymbols.textContent = countryCurrencySymbols[selectedCountry];
    });

    // By default, search button is disabled
    const searchButton = document.getElementById('search-button');
    if (searchButton) {
        searchButton.disabled = true;

        // Enable button only if there is text in the input field
        const searchField = document.querySelectorAll('.search-field');
        searchField.forEach(input => {
          input.onkeyup = () => {
            if (input.value.trim().length > 0)
                searchButton.disabled = false;
            else
                searchButton.disabled = true;
          };
        })
    };
    
    const categoryButtons = document.querySelectorAll('.categories');
    categoryButtons.forEach(button => {
        button.onclick = () => {
          const tag = button.dataset.tag;
          loadListings('category', selectedCountry, tag);
        };
    });
    
    const userProfile = document.getElementById('user');
    if (userProfile) {
      userProfile.addEventListener('click', () => {
        loadListings('saved', selectedCountry);
      });
    };
    
                        
    searchButton.onclick = () => {
        const titleInput = document.getElementById('titleInput').value.trim();
        const locationInput = document.getElementById('locationInput').value.trim();

        loadListings('search', selectedCountry, 'n', encodeURIComponent(titleInput), locationInput);
    };

    const advancedButton = document.getElementById('advanced-button');
    if (advancedButton){
      advancedButton.onclick = () => {
        loadListings(
          'advanced',
          document.getElementById('country').value.trim(),
          document.getElementById('category').value.trim(),
          encodeURIComponent(document.getElementById('what').value.trim()),
          document.getElementById('where').value.trim(), 1,
          document.getElementById('results_per_page').value.trim(),
          encodeURIComponent(document.getElementById('what_and').value.trim()),
          encodeURIComponent(document.getElementById('what_phrase').value.trim()),
          encodeURIComponent(document.getElementById('what_or').value.trim()),
          encodeURIComponent(document.getElementById('what_exclude').value.trim()),
          encodeURIComponent(document.getElementById('title_only').value.trim()),
          document.getElementById('distance').value.trim(),
          document.getElementById('location0').value.trim(),
          document.getElementById('location1').value.trim(),
          document.getElementById('location2').value.trim(),
          document.getElementById('location3').value.trim(),
          document.getElementById('location4').value.trim(),
          document.getElementById('location5').value.trim(),
          document.getElementById('location6').value.trim(),
          document.getElementById('location7').value.trim(),
          document.getElementById('max_days_old').value.trim(),
          document.getElementById('sort_dir').value.trim(),
          document.getElementById('sort_by').value.trim(),
          document.getElementById('salary_min').value.trim(),
          document.getElementById('salary_max').value.trim(),
          document.getElementById('salary_include_unknown').checked ? '1' : 'n',
          document.getElementById('full_time').checked ? '1' : 'n',
          document.getElementById('part_time').checked ? '1' : 'n',
          document.getElementById('contract').checked ? '1' : 'n',
          document.getElementById('permanent').checked ? '1' : 'n',
          document.getElementById('company').value.trim()
        );

        // Close the dropdown
        document.getElementById('dropdown-button').classList.remove('show');
        document.getElementById('dropdown').classList.remove('show');
      };
    };
    

    loadListings('all', selectedCountry);

});


function changeCountry() {
    document.getElementById("country-form").submit();
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

function bookmarkToggle(id, category, title, salary_max, company, location, description) {
  const csrfToken = getCookie('csrftoken');

  description = description.replace(/\//g, 'garismiring');
  fetch(`/save_listing/${id}/${encodeURIComponent(category)}/${encodeURIComponent(title)}/${salary_max}/${company}/${location}/${encodeURIComponent(description)}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken,
    },
  })
    .then(response => response.json())
    .then(data => {
      const saveButton = document.getElementById(`save-${id}`);
      // Handle the response from the server, such as updating the UI or displaying a message

      if (data.success) {
        if (data.is_saved) {
          console.log('Job listing saved');
          saveButton.innerHTML = '<i class="fas fa-bookmark"></i>';
        } else {
          console.log('Job listing removed from saved listings');
          saveButton.innerHTML = '<i class="far fa-bookmark"></i>';
        }
      } else {
        // Bookmark toggle failed, handle the error or display an error message
        console.log('User is not authenticated');
      }
    })
    .catch(error => {
      // Handle any errors that occurred during the request
      console.error('Error toggling bookmark:', error);
    });
}

function loadListings(
  type, selectedCountry, tag = null, titleInput = null, locationInput = null, page = 1,
  results_per_page = null, what_and = null, what_phrase = null, what_or = null, what_exclude = null,
  title_only = null, distance = null, location0 = null, location1 = null, location2 = null,
  location3 = null, location4 = null, location5 = null, location6 = null, location7 = null,
  max_days_old = null, sort_dir = null, sort_by = null, salary_min = null, salary_max = null,
  salary_include_unknown = null, full_time = null, part_time = null, contract = null, permanent = null,
  company = null
) {
  const loadingGif = document.getElementById("loading-gif");
  const jobsView = document.getElementById("jobs-view");
  const pagination = document.querySelector(".pagination");
  const footer = document.querySelector(".blog-footer");
  footer.style.display = "none";
  loadingGif.style.display = "block";
  pagination.innerHTML = ""; // Clear existing content
  jobsView.innerHTML = ""; // Clear existing content
  fetch(`/get_listings/${type}/${selectedCountry}/${tag == null || tag == '' ? 'n/' : tag + '/'}` +
      `${titleInput == null || titleInput == '' ? 'n/' : titleInput + '/'}` +
      `${locationInput == null || locationInput == '' ? 'n/' : locationInput + '/'}${page + '/'}` +
      `${results_per_page == null || results_per_page == '' ? 'n/' : results_per_page + '/'}` +
      `${what_and == null || what_and == '' ? 'n/' : what_and + '/'}` +
      `${what_phrase == null || what_phrase == '' ? 'n/' : what_phrase + '/'}` +
      `${what_or == null || what_or == '' ? 'n/' : what_or + '/'}${what_exclude == null || what_exclude == '' ? 'n/' : what_exclude + '/'}` +
      `${title_only == null || title_only == '' ? 'n/' : title_only + '/'}${distance == null || distance == '' ? 'n/' : distance + '/'}` +
      `${location0 == null || location0 == '' ? 'n/' : location0 + '/'}${location1 == null || location1 == '' ? 'n/' : location1 + '/'}` +
      `${location2 == null || location2 == '' ? 'n/' : location2 + '/'}${location3 == null || location3 == '' ? 'n/' : location3 + '/'}` +
      `${location4 == null || location4 == '' ? 'n/' : location4 + '/'}${location5 == null || location5 == '' ? 'n/' : location5 + '/'}` +
      `${location6 == null || location6 == '' ? 'n/' : location6 + '/'}${location7 == null || location7 == '' ? 'n/' : location7 + '/'}` +
      `${max_days_old == null || max_days_old == '' ? 'n/' : max_days_old + '/'}${sort_dir == null || sort_dir == '' ? 'n/' : sort_dir + '/'}` +
      `${sort_by == null || sort_by == '' ? 'n/' : sort_by + '/'}${salary_min == null || salary_min == '' ? 'n/' : salary_min + '/'}` +
      `${salary_max == null || salary_max  == '' ? 'n/' : salary_max + '/'}${salary_include_unknown == '1' ? '1/' : 'n/'}` +
      `${full_time == '1' ? '1/' : 'n/'}${part_time == '1' ? '1/' : 'n/'}${contract == '1' ? '1/' : 'n/'}${permanent == '1' ? '1/' : 'n/'}` +
      `${company == null || company  == '' ? 'n/' : company + '/'}`)
    .then(response => response.json())
    .then(data => {
      loadingGif.style.display = "none";
      footer.style.display = "block";
      
      const jobsCount = document.createElement("div");
      jobsCount.classList.add("col-12", "text-end", "mb-3", "fst-italic");
      jobsCount.textContent = `${data.count.toLocaleString()} jobs found.`;
      jobsView.appendChild(jobsCount);
      jobsView.classList.add("row");

      // Check if results are empty
      if (data.results.length === 0) {
        const notFoundMessage = document.createElement("div");
        notFoundMessage.classList.add("col-12", "text-center");
        notFoundMessage.textContent = "No listings found.";
        jobsView.appendChild(notFoundMessage);
      } else {
        // Create job elements
        data.results.forEach(result => {
          const jobElement = document.createElement("div");
          jobElement.classList.add("col-md-3", "mb-4");
          const categoryLabel = result.category.label || result.category;
          const modifiedLabel = categoryLabel.replace(" Jobs", "");
          jobElement.innerHTML = `
            <div class="card">
              <div class="card-body pb-2" id="listing-${result.id}">
                <div class="card-content mb-3">
                  ${modifiedLabel !== 'Unknown' ? `<strong class="d-inline-block mb-2 text-primary">${modifiedLabel}</strong>` : ""}
                  <h5 class="card-title">${result.title} <span class="text-success">
                    ${result.salary_max ? `Up to ${countryCurrencySymbols[selectedCountry]}${result.salary_max.toLocaleString()}` : ""}</span>
                  </h5>
                  ${result.company.display_name !== undefined ? `<p class="card-subtitle text-muted">${result.company.display_name}</p>` : ""}
                  ${result.company.__CLASS__ == null ? `<p class="card-subtitle text-muted">${result.company}</p>` : ""}
                  <p class="card-subtitle text-muted mb-2">${result.location.display_name || result.location}</p>
                  <p class="card-text">${result.description}</p>
                </div>
                <a href="${result.redirect_url}" class="text-decoration-none" onMouseOver="this.style.color='blue'" onMouseOut="this.style.color='#0275d8'">
                  View Job
                </a>
              </div>
            </div>
          `;
          

          if (data.is_authenticated) {
            const cardBody = jobElement.querySelector(`#listing-${result.id}`);
          
            if (cardBody) {
              const saveSpan = document.createElement('span');
              saveSpan.classList.add('float-end');
              const saveButton = document.createElement('button');
              saveButton.classList.add('btn', 'btn-link', 'save-button', 'text-dark');
              saveButton.setAttribute('data-bs-toggle', 'tooltip');
              saveButton.setAttribute('data-bs-placement', 'top');
              saveButton.id = `save-${result.id}`;
          
              saveButton.addEventListener('click', () => {
                bookmarkToggle(
                  result.id,
                  result.category.label || result.category,
                  result.title,
                  result.salary_max,
                  result.company.display_name|| result.company,
                  result.location.display_name || result.location,
                  result.description
                );
              });

              // Check if the listing is saved and set the appropriate classes
              if (!data.saved_job_listings.includes(result.id)) {
                saveButton.innerHTML = '<i class="far fa-bookmark"></i>';
                saveButton.setAttribute('data-bs-title', 'Save job listing');
              } else {
                saveButton.innerHTML = '<i class="fas fa-bookmark"></i>';
                saveButton.setAttribute('data-bs-title', 'Remove from saved listings');
              }
          
              saveSpan.appendChild(saveButton);
              cardBody.appendChild(saveSpan);

              // Enable tooltip
              const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
              tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
              });
            }
          }
          jobsView.appendChild(jobElement);
        });
      }
      if (page > 1) {
        const firstButton = document.createElement('a');
        firstButton.classList.add('page-link');
        firstButton.innerHTML = '&laquo; First';
        pagination.appendChild(firstButton);
        firstButton.onclick = () => {
          loadListings(type, selectedCountry, tag, titleInput, locationInput, 1);
          window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top of the page
        };
        const previousButton = document.createElement('a');
        previousButton.classList.add('page-link');
        previousButton.innerHTML = 'Previous';
        pagination.appendChild(previousButton);
        previousButton.onclick = () => {
          loadListings(type, selectedCountry, tag, titleInput, locationInput, page - 1);
          window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top of the page
        };
      }

      const pages = document.createElement('li');
      pages.classList.add('page-item');
      pages.innerHTML = `
        <small><span class="page-current text-muted page-link">
          Page ${page.toLocaleString()} of ${data.num_pages.toLocaleString()}
        </span></small>
      `;
      pagination.appendChild(pages);

      if (page < data.num_pages) {
        const nextButton = document.createElement('a');
        nextButton.classList.add('page-link');
        nextButton.innerHTML = 'Next';
        nextButton.onclick = () => {
          loadListings(type, selectedCountry, tag, titleInput, locationInput, page + 1);
          window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top of the page
        };
        const lastButton = document.createElement('a');
        lastButton.classList.add('page-link');
        lastButton.innerHTML = 'Last &raquo;';
        lastButton.onclick = () => {
          loadListings(type, selectedCountry, tag, titleInput, locationInput, data.num_pages);
          window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top of the page
        };
        pagination.appendChild(nextButton);
        pagination.appendChild(lastButton);
      }
    })
    .catch(error => {
      loadingGif.style.display = "none";
      console.error("Error loading listings:", error);
    });
}
