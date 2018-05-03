from src import unpickle
from src import train_category
from importlib import reload
from sklearn import tree as t
import numpy as np
import src.game as g


def Train_models(max_depth = 3):
    Traits = ['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']
    models = []

    for trait in Traits:
        y = traits_df[trait].values*100
        y = [int(x) for x in y]
        X = questions.values

        # train the model

        model,X_test,y_test = train_category.train_category(X,y,traits_df,max_depth)

        #export the tree
        t.export_graphviz(model,out_file='tree.dot')
        print(trait)
        error = np.round(np.mean(np.abs(model.predict(X_test)-y_test)),2)
        print('Mean abs error: '+str(error)+'%','\n','-'*50)
        models.append(model)
    return Traits,models

if __name__ == '__main__':

    #load in the pickled make_user_profiles
    long_key, questions, grading_Key,\
    keys2trait, Trait_dict_keys, Trait_dict_questions,\
    graded_df, percentile_df, traits_df= unpickle.Load_pickled_files()

    #ask for the number of questions
    print('\n\n\n\n','-'*50)
    print("How many questions would you like (max) per trait")
    max_depth = -1
    while (max_depth < 0) or (max_depth > 15):
        max_depth = input('Enter a integer between 2 and 15: ')
        max_depth = int(max_depth)


    print('\n','-'*50,'\n')

    print('Would you like to play the game for all traits or only one?')


    Number = -1
    while (Number != 'a') and (Number != '1'):
        Number = input('Enter either "a" for all or "1" for one ')


    Traits,models = Train_models(max_depth - 1)

    if Number == '1':
        tree = models[0].tree_
        print(Traits[0])
        quiz = g.Quiz()
        quiz.play_game(tree,long_key,questions)

    else:
        for i,model in enumerate(models):
            tree = model.tree_
            print(Traits[i])

            if i == 0:
                quiz = g.Quiz()
                df = quiz.play_game(tree,long_key,questions)
            else:
                df = quiz.play_game(tree,long_key,questions,(True,df),Traits[i])
            print(Traits[i])
            print('\n\n')
