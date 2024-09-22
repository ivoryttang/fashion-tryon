const { chromium } = require('playwright');
require('dotenv').config();

/**
 * Searches for a similar outfit to virtual try on from Amazon.com
 * @param {*} query search term on Amazon
 */
async function amazonSearch({ 
    query = "White silk pant suit for women"
}) {
    const browser = await chromium.connectOverCDP(`wss://connect.browserbase.com?apiKey=${process.env.BROWSERBASE_API_KEY}`);
    console.info('Connected!');
    try {
        const context = browser.contexts()[0];
        const page = context.pages()[0];

        try {
            const context = browser.contexts()[0];
            const page = context.pages()[0];
        
            // Navigate to Amazon
            await page.goto('https://www.amazon.com');
        
            try {
                // Wait for a short time to see if the popup appears
                await page.waitForSelector('[aria-label="Dismiss sign in"]', { timeout: 3000 });
                
                // Close the popup if it appears
                await page.click('[aria-label="Dismiss sign in"]');
                console.log('Popup dismissed');
            } catch (error) {
                // If the popup does not appear, continue with the search
                console.log('No signup popup appeared');
            }
        
            await page.fill('input[name="field-keywords"]', query); 
            await page.press('input[name="field-keywords"]', 'Enter');
            // Search for the outfit
            // await page.fill('input#twotabsearchtextbox', "cute fall knitted dress");
            // await page.click('input#nav-search-submit-button');
            await page.waitForSelector('div[data-component-type="s-search-result"]');
        
            // Select the first search result link
            const firstResultSelector = 'div[data-component-type="s-search-result"] a.a-link-normal';
        
            // Ensure the first search result is visible and clickable
            const firstResultElement = await page.$(firstResultSelector);
            console.log("found first result")
        
            if (firstResultElement) {
                // Scroll the element into view
                await firstResultElement.scrollIntoViewIfNeeded();
        
                // Click the first search result
                await firstResultElement.click();
                console.log('Clicked on the first search result.');
            } else {
                console.log('First search result not found.');
            }
        
            
            // Select size
            page.locator("#dropdown_selected_size_name span").nth(1).click()
            page.get_by_label("Small").get_by_text("Small").click()
        
            // Wait for product page to load
            await page.waitForSelector('#add-to-cart-button', { visible: true });
        
            // Add to cart
            page.get_by_role("link", name="Add to Cart").click()
        
            // Keep the browser open for a while so you can see the result
            await page.waitForTimeout(10000);
        
          } catch (error) {
            console.error('An error occurred:', error);
          } finally {
            await browser.close();
          }

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        await browser.close();
    }
}

// Run the function
amazonSearch({ query: "Women's summer floral dress" }).then(url => { // replace with similar search term
    console.log("Final Cart Button URL:", url);
}).catch(error => {
    console.error("Error in amazonSearch:", error);
});