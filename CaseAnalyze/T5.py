from modelscope.models import Model
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

pipeline_ins = pipeline(task=Tasks.text2text_generation, model='langboat/mengzi-t5-base')
result = pipeline_ins(input='中国的首都位于<extra_id_0>。')
print (result)
#{'text': '北京'}


from modelscope.models.nlp import T5ForConditionalGeneration
from modelscope.preprocessors import TextGenerationTransformersPreprocessor
model = T5ForConditionalGeneration.from_pretrained('langboat/mengzi-t5-base')
preprocessor = TextGenerationTransformersPreprocessor(model.model_dir)
pipeline_ins = pipeline(
    task=Tasks.text2text_generation,
    model=model,
    preprocessor=preprocessor)
print(pipeline_ins('中国的首都位于<extra_id_0>。'))
#{'text': '北京'}
