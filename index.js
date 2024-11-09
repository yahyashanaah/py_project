const inputs = ['I:Hello', 'I:World', 'U', 'I:Coding'];
let result = [];

inputs.forEach(item => {
    if (item.startsWith('I:')) {
        result.push(item.substring(2));
    }
    else if (item === 'U') {
        result.pop();
    }
}
);
const output = result.join(' ');
console.log(output);