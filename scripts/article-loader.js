// Article loading and navigation management
class ArticleManager {
  constructor() {
    this.articlesConfig = null;
    this.currentCategory = null;
    this.currentArticle = null;
    this.init();
  }

  async init() {
    await this.loadArticlesConfig();
    this.generateNavigation();
    this.handleRouting();
  }

  async loadArticlesConfig() {
    try {
      const response = await fetch('../articles/articles-config.json');
      this.articlesConfig = await response.json();
    } catch (error) {
      console.error('Failed to load articles configuration:', error);
    }
  }

  generateNavigation() {
    const navElement = document.getElementById('main-nav');
    if (!navElement || !this.articlesConfig) return;

    const navHTML = `
      <ul>
        <li><a href="../index.html">Home</a></li>
        ${Object.entries(this.articlesConfig.categories).map(([categoryKey, category]) => `
          <li class="dropdown">
            <a href="#" data-category="${categoryKey}">${category.displayName}</a>
            <ul class="dropdown-menu">
              ${category.articles.map(article => `
                <li><a href="?category=${categoryKey}&article=${article.id}" data-category="${categoryKey}" data-article="${article.id}">${article.title}</a></li>
              `).join('')}
            </ul>
          </li>
        `).join('')}
      </ul>
    `;
    
    navElement.innerHTML = navHTML;
    
    // Add click handlers for article links
    navElement.addEventListener('click', (e) => {
      if (e.target.dataset.article) {
        e.preventDefault();
        this.loadArticle(e.target.dataset.category, e.target.dataset.article);
        // Update URL without page reload
        const newUrl = `?category=${e.target.dataset.category}&article=${e.target.dataset.article}`;
        window.history.pushState({}, '', newUrl);
      }
    });
  }

  handleRouting() {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    const article = urlParams.get('article');
    
    if (category && article) {
      this.loadArticle(category, article);
    } else {
      // Show default content or redirect to home
      this.showDefaultContent();
    }
  }

  async loadArticle(categoryKey, articleId) {
    const category = this.articlesConfig.categories[categoryKey];
    if (!category) return;

    const article = category.articles.find(a => a.id === articleId);
    if (!article) return;

    this.currentCategory = categoryKey;
    this.currentArticle = articleId;

    // Update page title and header
    document.getElementById('article-title').textContent = `${article.title} | Andreia Otto`;
    document.getElementById('page-header').textContent = article.title;
    document.getElementById('page-subtitle').textContent = article.description;

    // Generate sidebar with category articles
    this.generateSidebar(categoryKey, articleId);

    // Load article content
    try {
      const response = await fetch(`../articles/${categoryKey}/${article.filename}`);
      const content = await response.text();
      document.getElementById('article-content').innerHTML = content;
    } catch (error) {
      console.error('Failed to load article:', error);
      document.getElementById('article-content').innerHTML = `
        <div class="error">
          <h2>Article Not Found</h2>
          <p>Sorry, the requested article could not be loaded.</p>
          <a href="../index.html">Return to Home</a>
        </div>
      `;
    }

    // Update active navigation state
    this.updateActiveNavigation(categoryKey, articleId);
  }

  generateSidebar(categoryKey, currentArticleId) {
    const sidebarElement = document.getElementById('article-sidebar');
    if (!sidebarElement || !this.articlesConfig) return;

    // Make sure sidebar is visible
    sidebarElement.style.display = 'block';

    const category = this.articlesConfig.categories[categoryKey];
    if (!category) return;

    const sidebarHTML = `
      <h3>${category.displayName} Articles</h3>
      <ul>
        ${category.articles.map(article => `
          <li>
            <a href="?category=${categoryKey}&article=${article.id}" 
               data-category="${categoryKey}" 
               data-article="${article.id}"
               class="${article.id === currentArticleId ? 'current' : ''}"
               title="${article.description}">
              ${article.title}
            </a>
          </li>
        `).join('')}
      </ul>
    `;
    
    sidebarElement.innerHTML = sidebarHTML;

    // Add click handlers for sidebar links
    sidebarElement.addEventListener('click', (e) => {
      if (e.target.dataset.article) {
        e.preventDefault();
        this.loadArticle(e.target.dataset.category, e.target.dataset.article);
        // Update URL without page reload
        const newUrl = `?category=${e.target.dataset.category}&article=${e.target.dataset.article}`;
        window.history.pushState({}, '', newUrl);
      }
    });
  }

  updateActiveNavigation(categoryKey, articleId) {
    // Remove existing active classes
    document.querySelectorAll('.navbar a').forEach(link => {
      link.classList.remove('active');
    });

    // Add active class to current article
    const activeLink = document.querySelector(`[data-category="${categoryKey}"][data-article="${articleId}"]`);
    if (activeLink) {
      activeLink.classList.add('active');
    }
  }

  showDefaultContent() {
    // Hide sidebar when not viewing an article
    const sidebarElement = document.getElementById('article-sidebar');
    if (sidebarElement) {
      sidebarElement.style.display = 'none';
    }

    document.getElementById('article-content').innerHTML = `
      <div class="default-content">
        <h2>Welcome to My Articles</h2>
        <p>Please select an article from the navigation menu above to read more about my experiences and insights.</p>
        <a href="../index.html">Return to Home</a>
      </div>
    `;
  }
}

// Initialize article manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ArticleManager();
});

// Handle browser back/forward buttons
window.addEventListener('popstate', () => {
  location.reload();
});