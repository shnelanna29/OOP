const enUpper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
const enLower = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];

function displayAlphabets() {
    let displayText = '';
    
    displayText += '<div class="alphabet-section"><strong>Английский алфавит (ROT13):</strong><br>';
    for (let i = 0; i < enUpper.length; i++) {
        const rotIndex = (i + 13) % enUpper.length;
        displayText += `${enUpper[i]}=${enUpper[rotIndex]}, ${enLower[i]}=${enLower[rotIndex]}${i < enUpper.length-1 ? ', ' : ''}`;
    }
    displayText += '</div>';
    
    document.getElementById("alphabetDisplay").innerHTML = displayText;
}

function findCharIndex(char, array) {
    for (let i = 0; i < array.length; i++) {
        if (char === array[i]) return i;
    }
    return -1;
}

function rot13Transform(input) {
    let output = '';
    const logEntries = [];
    
    for (let i = 0; i < input.length; i++) {
        let ch = input[i];
        let originalChar = ch;
        let logEntry = `${ch} = `;
        
        let enUpperIndex = findCharIndex(ch, enUpper);
        if (enUpperIndex !== -1) {
            const newIndex = (enUpperIndex + 13) % enUpper.length;
            ch = enUpper[newIndex];
            logEntry += `${ch} (${enUpperIndex}=${newIndex})`;
        } 
        else {
            let enLowerIndex = findCharIndex(ch, enLower);
            if (enLowerIndex !== -1) {
                const newIndex = (enLowerIndex + 13) % enLower.length;
                ch = enLower[newIndex];
                logEntry += `${ch} (${enLowerIndex}=${newIndex})`;
            }
            else {
                logEntry += `${ch} (no change)`;
            }
        }
        
        output += ch;
        logEntries.push(logEntry);
    }
    
    return { output, logEntries };
}

function updateOutput() {
    const input = document.getElementById("inputText").value;
    const { output, logEntries } = rot13Transform(input);
    
    document.getElementById("outputText").textContent = output;
    
    const logContainer = document.getElementById("logEntries");
    logContainer.innerHTML = '';
    logEntries.forEach(entry => {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.textContent = entry;
        logContainer.appendChild(div);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    displayAlphabets();
    
    document.getElementById("transformBtn").addEventListener("click", updateOutput);
    
    document.getElementById("inputText").addEventListener("input", function() {
        updateOutput();
    });
});

