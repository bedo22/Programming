// ponytail: small quiz + predict-output widget. No deps. Reads options from data attributes. Reused by every lesson.
(function(){
  var MSG = {
    correctQuiz: 'Correct. ',
    wrongQuiz: 'Not quite — try again. (Pick another option or reveal the answer below.)',
    correctPredict: 'Correct — that is exactly what runs.',
    wrongPredict: 'Not quite. Expected: '
  };
  function markSelected(optionInputs){
    optionInputs.forEach(inp=>{
      if(inp.checked) inp.closest('label').classList.add('selected');
      else inp.closest('label').classList.remove('selected');
    });
  }
  function setupQuiz(q){
    var labels = q.querySelectorAll(':scope > .quiz-body > .quiz-options > label');
    var inputs = q.querySelectorAll(':scope > .quiz-body > .quiz-options input[type=radio]');
    var feedback = q.querySelector(':scope > .quiz-body > .quiz-feedback');
    var reveal = q.querySelector(':scope > .quiz-body > .quiz-reveal');
    var answer = q.getAttribute('data-answer');
    var explanation = q.getAttribute('data-explain') || '';
    inputs.forEach(function(inp){
      inp.addEventListener('change', function(){
        markSelected(inputs);
        var correct = inp.value === answer;
        feedback.textContent = correct ? MSG.correctQuiz.trim() : MSG.wrongQuiz;
        feedback.className = 'quiz-feedback ' + (correct ? 'correct' : 'wrong');
        if(reveal){
          if(correct){
            reveal.textContent = explanation;
            reveal.className = 'quiz-reveal';
            reveal.style.display = 'block';
          } else {
            reveal.style.display = 'none';
          }
        }
      });
    });
  }
  function setupPredict(p){
    var input = p.querySelector('input[type=text]');
    var btn   = p.querySelector('button');
    var fb    = p.querySelector('.predict-feedback');
    var reveal= p.querySelector('.predict-reveal');
    var expected = p.getAttribute('data-expected').trim();
    if(reveal) reveal.style.display='none';
    function norm(s){ return String(s).replace(/\s+/g,' ').trim(); }
    function check(){
      var got = norm(input.value);
      var ok = got === norm(expected);
      fb.textContent = ok ? MSG.correctPredict : (MSG.wrongPredict + expected);
      fb.className = 'predict-feedback ' + (ok ? 'correct' : 'wrong');
      if(reveal) reveal.style.display = ok ? 'none':'block';
    }
    btn.addEventListener('click', check);
    input.addEventListener('keydown', function(e){ if(e.key==='Enter') check(); });
  }
  document.querySelectorAll('.quiz').forEach(setupQuiz);
  document.querySelectorAll('.predict').forEach(setupPredict);
})();
