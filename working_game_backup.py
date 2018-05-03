working_game_backup
import pandas as pd
import numpy as np

Traits = ['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism']

class Quiz:

    def __init__(self):
        self.print_flag = 0
        self.Trait_score = []
        self.Traits = []


    def play_game(self,model,long_key,questions,trait,df = (False,0)):
        # set some of the variables to the correct values
        self.model = model
        self.tree = model.tree_
        self.root = 0
        self.long_key = long_key
        self.questions_index = questions.columns.values

        #if we already have some answers, use them, otherwise make a new dataframe
        if df[0] != False:
            self.df = df[1]
        else:
            self.df = pd.DataFrame([np.zeros(len(self.questions_index))],columns = self.questions_index)

        # If the print flag is set to one, don't print the initial statement
        if self.print_flag == 0:
            self.print_initial_statement()
            self.print_flag = 1
        else: print('next trait: ',trait)
        #append the trait to the object
        self.Traits.append(trait)

        #call the trait test
        self.Trait_Test()

        #return some valuable information
        return self.df,zip(self.Traits,self.Trait_score)
    def Trait_Test(self):
        '''
        Run the trait test for a specific trait

        '''
        # Make sure not a leaf:
        while self.tree.feature[self.root] != -2:

            #reassign the left and right child
            left_child = self.tree.children_left[self.root]
            right_child = self.tree.children_right[self.root]

            # Get the question number, query the long key and steal the key index
            key_idx = self.long_key.Item == self.questions_index[self.tree.feature[self.root]]

            #Get the key as a string
            string_key = list(self.long_key.loc[key_idx,:].Sign.values)

            #decide if the question is reverse scored
            reverse_score = list(string_key[0])[0] == '-'

            if (self.df[self.questions_index[self.tree.feature[self.root]]].values == 0):
                # call the function to get an answer
                user_answer = self.get_answer()
            else:
                 user_answer = self.df[self.questions_index[self.tree.feature[self.root]]]
                 user_answer = float(user_answer)

            #if needs to be reversed, do it
            if reverse_score == True:
                user_answer = self.reverse_score(user_answer)

            #See which node to choose next
            if user_answer < self.tree.threshold[self.root]:
                self.root = left_child

            else:
                self.root= right_child

        # Save out the Percentile Score
        Percentile_score = np.round(self.tree.value[self.root][0][0],3)
        self.Trait_score.append(Percentile_score)
        std_score = np.round(self.tree.impurity[self.root]**(1/2),2)
        print('\nRMSE = ',std_score,'\n')
        #Save out the node
        node = self.root



        print("\nYou fall in the "+str(Percentile_score)+ '% percentile of this trait'+\
        ' which correponds to node: '+str(node) )


    def reverse_score(self,value):
        '''
        Returns reversed score
        '''
        return 6 - value

    def get_answer(self):
        '''
        Ask for the input from the user.  Allowed to be a float, but makes sure
        it is a number
        '''
        #Set value for the loop
        value = -1

        #Keep track of how many tries the user has done
        imput_count = 0

        #do a while loop to check the value
        while (value < 1) | (value > 5):

            #if user has tried multiple times, give them a prompt with the
            #rules
            if imput_count > 0:
                name = 'Answer needs to be an integer between 1 & 5'
                value = input(name+'\n'+self.questions_index[self.tree.feature[self.root]]+' ')
            #Otherwise just ask for the input
            else:
                value = input(self.questions_index[self.tree.feature[self.root]]+' ')

            #check to see if it is a number
            if value.isdigit():
                value = int(value)
            elif self.is_float(value):
                value = float(value)

            #otherwise set the value to -1
            else: value = -1

            #increment attempt count
            imput_count +=1

        self.df[self.questions_index[self.tree.feature[self.root]]] = value
        return value




    def is_float(self,string):
        '''
        See if the value is a float
        '''
        try:
            float(string)
            return True
        except ValueError:
            return False


    def print_initial_statement(self):
        Words = '''Hello, welcome to the quiz game!  Answer the following questions
        to better understand where you fall in the personality thing \n'''
        print(Words)
        Words = '''For each statement, rank the statement based on 1-5 scale
        \n\n 1 = Very Innacurate and 5 = Very accurate\n\n'''
        print(Words)
        print('-'*50,'\n\n')
