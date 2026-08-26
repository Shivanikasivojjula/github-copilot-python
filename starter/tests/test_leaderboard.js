const assert = require('assert');
const {
  LEADERBOARD_KEY,
  loadLeaderboard,
  saveScore,
  formatTime
} = require('../static/main.js');

function storage() {
  const values = {};
  return {
    getItem: (key) => values[key] || null,
    setItem: (key, value) => { values[key] = value; }
  };
}

const testStorage = storage();
const scores = [
  { playerName: 'Slow', completionTime: 90, difficulty: 'easy', hints: 1 },
  { playerName: 'Fast', completionTime: 20, difficulty: 'hard', hints: 0 }
];
testStorage.setItem(LEADERBOARD_KEY, JSON.stringify(scores));
assert.deepStrictEqual(loadLeaderboard(testStorage).map((score) => score.playerName), ['Fast', 'Slow']);

for (let index = 0; index < 10; index += 1) {
  saveScore({ playerName: `Player ${index}`, completionTime: 30 + index, difficulty: 'medium', hints: index }, testStorage);
}
const topTen = loadLeaderboard(testStorage);
assert.strictEqual(topTen.length, 10);
assert.strictEqual(topTen[0].completionTime, 20);
assert.strictEqual(topTen[9].completionTime, 38);
assert.strictEqual(formatTime(125), '02:05');

testStorage.setItem(LEADERBOARD_KEY, 'not json');
assert.deepStrictEqual(loadLeaderboard(testStorage), []);
console.log('Leaderboard tests passed');