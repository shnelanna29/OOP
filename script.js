const alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                 'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

document.addEventListener('DOMContentLoaded', function() {
    const userInputField = document.getElementById('userInput');
    const resultDisplay = document.getElementById('resultDisplay');
    const transformButton = document.getElementById('transformButton');
    const transformationSteps = document.getElementById('transformationSteps');
    
    const alphabetInfo = document.createElement('div');
    alphabetInfo.className = 'alphabet-info';
    alphabetInfo.innerHTML = '<h3>Используемый алфавит:</h3><p>' + alphabet.join(' ') + '</p>';
    document.querySelector('.container').insertBefore(alphabetInfo, transformationSteps);

    function applyRot13Transformation(text) {
        let transformedText = '';
        transformationSteps.innerHTML = '<h3>Шаги преобразования:</h3><div class="steps-container"></div>';
        const stepsContainer = transformationSteps.querySelector('.steps-container');
        
        for (let idx = 0; idx < text.length; idx++) {
            const currentChar = text[idx];
            let uppercaseChar = currentChar.toUpperCase();
            let isLowerCase = currentChar !== uppercaseChar;
            let transformationInfo = '';
            
            if (alphabet.includes(uppercaseChar)) {
                const charIndex = alphabet.indexOf(uppercaseChar);
                const newIndex = (charIndex + 13) % 26;
                const newChar = alphabet[newIndex];
                transformedText += isLowerCase ? newChar.toLowerCase() : newChar;
                transformationInfo = `<span>${currentChar} → ${isLowerCase ? newChar.toLowerCase() : newChar}</span>`;
            } else {
                transformedText += currentChar;
                continue;
            }
            
            stepsContainer.innerHTML += transformationInfo;
        }
        
        return transformedText;
    }

    transformButton.addEventListener('click', function() {
        if (userInputField.value.trim() === '') {
            alert('Пожалуйста, введите текст для шифрования');
            return;
        }
        resultDisplay.textContent = applyRot13Transformation(userInputField.value);
    });
});
