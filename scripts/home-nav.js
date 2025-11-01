// Home page navigation management
class HomeNavigation {
  constructor() {
    this.articlesConfig = null;
    this.init();
  }

  async init() {
    await this.loadArticlesConfig();
    this.generateNavigation();
  }

  async loadArticlesConfig() {
    try {
      const response = await fetch('articles/articles-config.json');
      this.articlesConfig = await response.json();
    } catch (error) {
      console.error('Failed to load articles configuration:', error);
      // Fallback to static navigation if config fails
      this.generateFallbackNavigation();
    }
  }

  generateNavigation() {
    const navElement = document.getElementById('main-nav');
    if (!navElement || !this.articlesConfig) return;

    const navHTML = `
      <ul>
        <li><a href="index.html" class="active">Home</a></li>
        ${Object.entries(this.articlesConfig.categories).map(([categoryKey, category]) => `
          <li class="dropdown">
            <a href="#" data-category="${categoryKey}">${category.displayName}</a>
            <ul class="dropdown-menu">
              ${category.articles.map(article => `
                <li><a href="article-template.html?category=${categoryKey}&article=${article.id}">${article.title}</a></li>
              `).join('')}
            </ul>
          </li>
        `).join('')}
      </ul>
    `;
    
    navElement.innerHTML = navHTML;
  }

  generateFallbackNavigation() {
    const navElement = document.getElementById('main-nav');
    if (!navElement) return;

    // Fallback static navigation
    const navHTML = `
      <ul>
        <li><a href="index.html" class="active">Home</a></li>
        <li class="dropdown">
          <a href="#">Technology</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=technology&article=sre-basics">Site reliability engineering (SRE)</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Finance</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=finance&article=financial-independence">Finance Basics</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Health</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=health&article=wellness-fundamentals">Wellness Fundamentals</a></li>
            <li><a href="article-template.html?category=health&article=nutrition-basics">Nutrition Basics</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Living Abroad</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=living-abroad&article=expat-life">Living Abroad</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Dogs</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=dogs&article=dog-care">Dogs</a></li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#">Sailing</a>
          <ul class="dropdown-menu">
            <li><a href="article-template.html?category=sailing&article=sailing-adventures">Sailing</a></li>
          </ul>
        </li>
      </ul>
    `;
    
    navElement.innerHTML = navHTML;
  }
}

// Initialize home navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new HomeNavigation();
});