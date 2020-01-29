import numpy as np
import matplotlib.pyplot as plt

def print_scores(clf_cv, acc=True, prec=True, rec=True):
    '''Print cross validation results.
       Valid only for CrossValidation.
    '''
    if acc:
        print('accuracy: %.3f' % clf_cv['test_accuracy_score'].mean())
    if prec:
        print('precision: %.3f' % clf_cv['test_precision_score'].mean())
    if rec:
        print('recall: %.3f' % clf_cv['test_recall_score'].mean())


def plot_most_imp_features(clf, threshold, features_list):
    ''' Plot the features that contribute above the threshold to the decision process'''
    feat_imp = clf.feature_importances_
    above_thres_scores = feat_imp[feat_imp>threshold]*100
    most_imp_feat = np.argwhere(feat_imp>threshold).flatten()
    above_thres_feat = features_list[most_imp_feat]             # -> List of the most important features
    
    ax = plt.axes()
    (markers, stemlines, baseline) = ax.stem(list(range(len(above_thres_scores))),
                                     above_thres_scores, use_line_collection=True)

    plt.setp(markers, marker='o', markersize=15, markeredgecolor="olive", markeredgewidth=1)
    plt.setp(stemlines, linestyle="-", color="olive", linewidth=1)


    # x - axis
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.set_xlim((-.5, len(above_thres_scores)))

    # y - axis
    y_max = max(above_thres_scores)+2
    ax.axes.set_ylim((0, y_max))
    old_ticks = ax.axes.get_yticks()
    ticks_labels = ['{}%'.format(digit) for digit in old_ticks]
    ax.axes.set_yticklabels(ticks_labels)
    ax.axes.set_ylabel('Importance')
    ax.axes.set_title('Features importance')

    for index, feature in enumerate(above_thres_feat):
        ax.annotate(feature, xy=(index, above_thres_scores[index]+1), annotation_clip=False, rotation=50)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    '''
        Save plot on file.
        Options:
        fig_id: filename
        tight_layout: True by default
        fig_extension: "png" by default
        resolution: 300 by default
    '''
    path = 'images/'+fig_id+'.'+fig_extension
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    
    
def save_on_txt(filename, arr, format = 'txt'):
    ''' Save a list in txt format.
        Options:
        filename
        arr: list to be saved
        format: "txt" by default
    '''
    doc = filename+'.'+format
    file = open(doc, "w")
    for date, ratio in arr:
        file.write(date+'\t'+str(ratio)+'\n')
    file.close()
    print('Saved on '+filename)
