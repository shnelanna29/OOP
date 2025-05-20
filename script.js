let alphabet = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
];
  
let alphabetText = '';
let i = 0;
while (i < alphabet.length) {
    alphabetText = alphabetText + alphabet[i] + ' ';
    i = i + 1;
}
document.getElementById('alphabet').innerText = alphabetText.trim();
  
function rot13(text) {
    let result = '';
    let operationsLog = "Начало шифрования ROT13:";
    let j = 0;
    
    operationsLog += `Исходный текст: "${text}"\n\n`;
    
    while (j < text.length) {
        let ch = text[j];
        operationsLog += `Обработка символа ${j+1}: '${ch}'\n`;
        
        let found = false;
        let k = 0;
        while (k < alphabet.length) {
            if (alphabet[k] === ch) {
                let isUpper = k < 26;
                let base = isUpper ? 0 : 26;
                let pos = k - base;
                let newPos = (pos + 13) % 26 + base;
                
                operationsLog += `  Найден в алфавите на позиции ${k}\n`;
                operationsLog += `  Заменяем на: '${alphabet[newPos]}'\n`;
                
                result = result + alphabet[newPos];
                found = true;
                break;
            }
            k = k + 1;
        }
        
        if (!found) {
            operationsLog += `  Символ не найден в алфавите, оставляем как есть\n`;
            result = result + ch;
        }
        
    }
    
    operationsLog += `Финальный результат: "${result}"\n`;
    document.getElementById('operations').innerText = operationsLog;
    return result;
}
  
let input = document.getElementById('input');
let output = document.getElementById('output');
  
input.addEventListener('input', function() {
    output.innerText = rot13(input.innerText);
});
