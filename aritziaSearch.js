const { chromium } = require('playwright');
require('dotenv').config();

/**
 * Searches for a similar outfit to virtual try on from Amazon.com
 * @param {*} searchTerm search term on Amazon
 */
async function aritziaSearch(searchTerm) {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();

    try {
        // Navigate to Aritzia website
        await page.goto('https://www.aritzia.com/us/en/default');

        // Function to handle popups
        async function handlePopups() {
            const popupSelectors = [
                '#onetrust-accept-btn-handler',  // Cookie consent
                'button[aria-label="Close"]',    // Generic close button
                '.modal-close',                  // Another common close button class
                '[data-testid="close-button"]'   // Test ID for close buttons
            ];

            for (const selector of popupSelectors) {
                try {
                    const popup = await page.$(selector);
                    if (popup) {
                        await popup.click();
                        console.log(`Closed popup with selector: ${selector}`);
                    }
                } catch (error) {
                    console.log(`No popup found for selector: ${selector}`);
                }
            }
        }

        // Handle initial popups
        await handlePopups();

        // Wait for and click on the search icon
        await page.waitForSelector('button[aria-label="Search"]');
        await page.click('button[aria-label="Search"]');

        // Wait for the search input field and enter the search term
        const searchInput = await page.waitForSelector('input[name="q"]');
        await searchInput.fill(searchTerm);
        await searchInput.press('Enter');

        // Handle popups after search
        await handlePopups();

        // Wait for search results to load
        await page.waitForSelector('.product-grid');

        // Click on the first product in the search results
        const firstProduct = await page.$('.product-grid a[data-product-sku]');
        if (firstProduct) {
            await firstProduct.click();
            console.log(`Clicked on the first product for '${searchTerm}'`);
        } else {
            console.log("No search results found.");
            return;
        }

        // Handle popups on product page
        await handlePopups();

        // Wait for the product page to load
        await page.waitForSelector('button[data-add-to-cart]');

        // Select a size if required (this may vary depending on the product)
        const sizeSelector = await page.$('button[data-size-selector]');
        if (sizeSelector) {
            await sizeSelector.click();
            // Select the first available size
            const firstSize = await page.$('button[data-size-selector]:not([disabled])');
            if (firstSize) {
                await firstSize.click();
            }
        }

        // Click the "Add to Bag" button
        const addToBagButton = await page.$('button[data-add-to-cart]');
        if (addToBagButton) {
            await addToBagButton.click();
            console.log("Added item to bag.");
        } else {
            console.log("Couldn't find 'Add to Bag' button.");
        }

        // Handle popups after adding to bag
        await handlePopups();

        // Wait for the cart to update
        await page.waitForSelector('.minicart__product-item', { timeout: 10000 });
        console.log("Process completed. Item should be in the cart.");

        // Keep the browser open for manual inspection
        await new Promise(resolve => {
            process.stdin.once('data', () => {
                console.log('Closing browser...');
                resolve();
            });
            console.log('Press Enter to close the browser...');
        });

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        await browser.close();
    }
}

// Run the function
aritziaSearch({ searchTerm: "black dress" }).then(url => { // replace with similar search term
    console.log("Final Cart Button URL:", url);
}).catch(error => {
    console.error("Error in amazonSearch:", error);
});