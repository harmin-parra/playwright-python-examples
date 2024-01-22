# playwright-python-examples

These are the Cypress (https://example.cypress.io/) sample tests, but they have been rewritten into [Playwright](https://playwright.dev/python/docs/intro) (python).

Be aware that some Cypress commands don't have an equivalent in Playwright, thus some workarounds are proposed whenever possible.

If you find a better solution or do you have an alternative solution to one of the tests, please share it with me by raising an [issue](https://github.com/harmin-parra/playwright-python-examples/issues).

---
### To execute the tests:

1. Install [Playwright](https://playwright.dev/python/docs/intro) for python.

2. Download the project

   ``git checkout git@github.com:harmin-parra/playwright-python-examples.git``

   or download and unzip the [zip file](https://github.com/harmin-parra/playwright-python-examples/archive/refs/heads/main.zip) of the project

3. Enter the folder of the project

   ``cd playwright-python-examples``

4. Execute the test

   * with headless browser

     ``pytest tests``

   * with headed browser

     ``pytest --headed tests``
