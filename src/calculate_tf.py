import os

def calculate_tf(text):
    words = text.split()
    tf_dict = {}
    for word in words:
        tf_dict[word] = tf_dict.get(word, 0) + 1
    return tf_dict

def calculate_tf_all_file(directory):
    for file in os.listdir(directory):
        file_path = f"{directory}/{file}"
        with open(file_path, 'r', encoding='utf-8') as file:
            words = file.read().split()
            tf_dict = {}
            for word in words:
                tf_dict[word] = tf_dict.get(word, 0) + 1

    return tf_dict

if __name__ == '__main__':
    # Example of text:
    text = "messieurs les présidents mesdames messieurs en ce jour où je prends la responsabilité assumer la plus haute charge de etat je me sens dépositaire une espérance élection présidentielle a pas vu la victoire une france contre une autre une idéologie contre une autre elle a vu la victoire une france qui veut se donner les moyens entrer forte et unie dans le troisième millénaire le 7 mai le peuple français a exprimé sa volonté de changement je suis décidé à placer le septennat qui commence sous le signe de la dignité de la simplicité de la fidélité aux valeurs essentielles de notre république je aurai autre ambition que de rendre les français plus unis plus égaux et la france plus allante forte de son histoire comme de ses atouts je ferai tout pour qun etat impartial assumant pleinement ses missions de souveraineté et de solidarité soit pour les citoyens le garant de leurs droits et le protecteur de leurs libertés je ferai tout pour que notre démocratie soit affermie et mieux équilibrée par un juste partage des compétences entre exécutif et le législatif ainsi que avait voulu le général de gaulle fondateur de la vème république le président arbitrera fixera les grandes orientations assurera unité de la nation préservera son indépendance le gouvernement conduira la politique de la nation le parlement fera la loi et contrôlera action gouvernementale telles sont les voies à suivre je veillerai à ce qune justice indépendante soit dotée des moyens supplémentaires nécessaires à accomplissement de sa tâche surtout engagerai toutes mes forces pour restaurer la cohésion de la france et renouer le pacte républicain entre les français emploi sera ma préoccupation de tous les instants la campagne qui achève a permis à notre pays de se découvrir tel qil est avec ses cicatrices ses fractures ses inégalités ses exclus mais aussi avec son ardeur sa générosité son désir de rêver et de faire du rêve une réalité la france est un vieux pays mais aussi une nation jeune enthousiaste prête à libérer le meilleur elle même pour peu qon lui montre horizon et non étroitesse de murs clos le président françois mitterrand a marqué de son empreinte les quatorze ans qui viennent de écouler un nouveau septennat commence je voudrais qà issue de mon mandat les français constatent que le changement espéré a été réalisé je voudrais que plus assurés de leur avenir personnel tous nos compatriotes se sentent partie prenante un destin collectif je voudrais que ces années lourdes enjeux mais ouvertes à tous les possibles les voient devenir plus confiants plus solidaires plus patriotes et en même temps plus européens car la force intérieure est toujours la source un élan vers extérieur avec aide des hommes et des femmes de bonne volonté conformément à esprit et à la lettre de nos institutions et aussi à idée que je me fais de ma mission je serai auprès des français garant du bien public en charge des intérêts supérieurs de la france dans le monde et de universalité de son message vive la république vive la france"
    print(calculate_tf(text))