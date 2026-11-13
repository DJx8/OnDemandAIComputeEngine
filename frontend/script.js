
const API_URL = "/compute/execute";

const directionSelect = document.getElementById("direction");
const languageSelect = document.getElementById("language");
const inputText = document.getElementById("input-text");
const outputText = document.getElementById("output-text");

const translateBtn = document.getElementById("translate-btn");
const buttonText = document.getElementById("button-text");
const clearBtn = document.getElementById("clear-btn");
const copyBtn = document.getElementById("copy-btn");

const charCount = document.getElementById("char-count");
const errorMessage = document.getElementById("error-message");
const resultStatus = document.getElementById("result-status");

const sourceLabel = document.getElementById("source-label");
const sourceLanguage = document.getElementById("source-language");
const targetLabel = document.getElementById("target-label");

const PLACEHOLDER_TEXT = "Your translation will appear here...";


// Show placeholder
function showPlaceholder() {
    outputText.textContent = PLACEHOLDER_TEXT;
    outputText.classList.add("placeholder");
}


// Show actual output
function showOutput(text) {
    outputText.textContent = text;
    outputText.classList.remove("placeholder");
}


// Update language labels based on direction
function updateDirection() {

    const direction = directionSelect.value;

    if (direction === "English → Indian Language") {

        sourceLabel.textContent = "From English";
        sourceLanguage.textContent = "English";
        targetLabel.textContent = "Translate to";

    } else {

        sourceLabel.textContent = "From Indian Language";
        sourceLanguage.textContent = languageSelect.value;
        targetLabel.textContent = "Translate to English";

    }
}


// Character counter
inputText.addEventListener("input", () => {

    charCount.textContent = `${inputText.value.length} / 5000`;

    if (directionSelect.value === "Indian Language → English") {
        sourceLanguage.textContent = languageSelect.value;
    }

});


// Language selection events
directionSelect.addEventListener("change", updateDirection);
languageSelect.addEventListener("change", updateDirection);


// Translation
translateBtn.addEventListener("click", async () => {

    const text = inputText.value.trim();
    const direction = directionSelect.value;
    const language = languageSelect.value;

    errorMessage.textContent = "";

    if (!text) {
        errorMessage.textContent = "Please enter some text to translate.";
        return;
    }

    translateBtn.disabled = true;
    buttonText.textContent = "Translating...";

    showOutput("Please wait while the AI translates your text...");

    resultStatus.textContent = "Processing";
    copyBtn.disabled = true;

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task: "translation",
                parameters: {
                    direction: direction,
                    text: text,
                    language: language
                }
            })
        });

        const data = await response.json();

        if (!response.ok) {

            if (response.status === 429) {
                throw new Error(
                    "Too many requests. Please wait a minute and try again."
                );
            }

            if (response.status === 502) {
                throw new Error(
                    "Translation service is temporarily unavailable. Please try again later."
                );
            }

            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Translation failed. Please check your input."
            );
        }

        if (data.status !== "success") {
            throw new Error(
                "The translation service returned an unexpected response."
            );
        }

        showOutput(data.result);

        resultStatus.textContent = "Translation completed";
        copyBtn.disabled = false;

    } catch (error) {

        showOutput("Translation could not be completed.");

        resultStatus.textContent = "Failed";
        errorMessage.textContent = error.message;

    } finally {

        translateBtn.disabled = false;
        buttonText.textContent = "Translate →";

    }

});


// Clear input and output
clearBtn.addEventListener("click", () => {

    inputText.value = "";

    showPlaceholder();

    charCount.textContent = "0 / 5000";
    resultStatus.textContent = "Ready to translate";

    errorMessage.textContent = "";
    copyBtn.disabled = true;

});


// Copy translated text
copyBtn.addEventListener("click", async () => {

    const translatedText = outputText.textContent;

    try {

        await navigator.clipboard.writeText(translatedText);

        copyBtn.textContent = "Copied!";

        setTimeout(() => {
            copyBtn.textContent = "Copy";
        }, 1500);

    } catch {

        errorMessage.textContent =
            "Unable to copy. Please copy the text manually.";

    }

});


// Initial setup
showPlaceholder();
updateDirection();
