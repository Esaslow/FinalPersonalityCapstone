import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt

def plot(trait_scores,percentile_df_user,keys2trait):

    locs = [(-5,4),(-5,-4),(0,0),(5,-4),(5,4)]

    w_scaling = 12
    h_scaling = 5


    #Define the traits and the colors
    Traits = np.array(['Openness','Conscientiousness','Extraversion','Agreeableness','Neuroticism'])
    colors = ['firebrick','olive','dodgerblue','magenta','sandybrown']
    angles = [0,45,180,240,300]

    #create the Eclipses
    est = [Ellipse(xy=loc, width=trait*w_scaling, height=trait*h_scaling)
        for loc,trait in zip(locs,trait_scores)]

    #Create the figure
    _,ax = plt.subplots(2,1,figsize = (10,10))

    #Add each of the eclispses to the figure
    for color,e in zip(colors,est):
        ax[0].add_artist(e)
        e.set_clip_box(ax[0].bbox)
        e.set_alpha(.4)
        e.set_facecolor(color)

    #Set the X and Y axis up
    ax[0].set_xlim(-10, 10)
    ax[0].set_ylim(-7, 7)

    #Go through and add the trait to the graph
    for score, trait,loc,color in zip(trait_scores,Traits,locs,colors):

        #Change the Location a little
        loc2 = (loc[0]-score*w_scaling/4,loc[1]+score*h_scaling/2+.1)

        #Add the text
        ax[0].annotate(trait+' '+str(np.round(score*100,2))+'%',
                    xy=loc2,color = color,size=20*(score+1/2))
        count = 1


    final_x_ticks = []
    final_x_labels = []
    colors = ['firebrick','olive','dodgerblue','magenta','sandybrown']
    count = 0
    for trait in Traits:
        values = []
        names = []
        for bla in percentile_df_user.index:
            if (trait[0] in bla):
                values.append(percentile_df_user.loc[bla])
                names.append(keys2trait[bla.split('-')[1]][1])


        ind = np.argsort(values)
        values = np.array(values)[ind]
        names = np.array(names)[ind]
        bottom = 5*count
        top = bottom+5
        pos = list(range(bottom,top))
        width = .9
        ax[1].bar(pos,
                #using 'openness data,
                values,
                # of width
                width,
                # with alpha 0.5
                alpha=0.5,
               color = colors[int(count/2)],
                 label = trait)
        count +=2
        final_x_ticks.append(pos)
        final_x_labels.append(names)

    ax[1].set_xticks(np.ndarray.flatten(np.array(final_x_ticks)));
    ax[1].set_xticklabels(np.ndarray.flatten(np.array(final_x_labels)),rotation = 90);

    ax[1].grid(alpha = .4,ls = '--',color = 'r')
    ax[1].legend();
    return ax
