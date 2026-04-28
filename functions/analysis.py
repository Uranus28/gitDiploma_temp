import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def getCSVFileName(vehicles):
    return '/all_sums_'+str(vehicles)+'.csv'

def get_fazes_folder(gridsDataFolder, green_faze = 30, red_faze = 30):
    return gridsDataFolder+"fazes_g"+str(green_faze)+"r_"+str(red_faze)


def get_dataFolder(gridsDataFolder, vehicles, green_faze = 30, red_faze = 30):
    return get_fazes_folder(gridsDataFolder, green_faze, red_faze)+"/dataFor_"+str(vehicles)+"_vehicles"

def plots(vehicles, pathToSave, green_faze = 30, red_faze = 30):
    vel=np.zeros(len(vehicles))
    nc=np.zeros(len(vehicles))
    flux=np.zeros(len(vehicles))
    save_imgs_folder = get_fazes_folder(pathToSave, green_faze, red_faze)
    for i in range(0,len(vehicles)):
        cur_count = vehicles[i]
        data_folder = get_dataFolder(pathToSave, cur_count, green_faze, red_faze)
        txt=np.loadtxt(data_folder+'/velm'+str(cur_count)+'.txt')
        nc[i] = np.mean(txt[95:100, 0])
        vel[i] = np.mean(txt[95:100, 1])
        flux[i]=np.mean(txt[95:100,2])
        # print(nc[i],vel[i],flux[i])

    # fig=plt.figure()
    plt.plot(nc/3000,vel,'o')
    plt.plot(nc / 3000, vel, color='k')
    plt.xlabel('Density')
    plt.ylabel('Velocity')
    plt.title('Скорость к плотности')
    plt.tight_layout()
    plt.savefig(save_imgs_folder+'/vel-density.png',dpi=600)

    fig=plt.figure()
    # Поток (flux) измеряет количество автомобилей, проходящих через определённую точку за конкретное время, 
    # — мера пропускной способности.
    plt.plot(nc / 3000,flux,'o',label='Traffic Simulation')
    plt.plot(nc / 3000, flux, color='k')
    plt.plot(vehicles/3000,vehicles*vel[0],'r--',label='No Interaction')
    plt.ylim(0,2800)
    plt.legend()
    plt.xlabel('Density')
    plt.ylabel('Flux')
    plt.title('Поток к плотности')
    plt.tight_layout()
    plt.savefig(save_imgs_folder+'/flux-density.png', dpi=600)
    
    plt.tight_layout() # Prevents label overlapping
    plt.show()

def plots_mean_traffic(durations, vehicles, pathToSave):
    col_names = np.insert(np.array(vehicles).astype(str), 0, "duration") 
    # Create the DataFrame
    dfAll = pd.DataFrame(columns=col_names)

    for duration in durations:
        duration_mean_array = []
        for i in range(0,len(vehicles)):
            cur_count = vehicles[i]
            data_folder = get_dataFolder(pathToSave, cur_count, green_faze=duration, red_faze=duration)
            df = pd.read_csv(data_folder + getCSVFileName(cur_count))
            duration_mean_array.append(df.iloc[0].mean())
        new_array = np.array(duration_mean_array)
        dfAll = pd.concat([dfAll, pd.DataFrame([np.insert(new_array, 0, duration)], columns=dfAll.columns)],
                           ignore_index=True)
    print(dfAll)
    dfAll.set_index('duration').plot(ylabel='Mean машин, проехавших через светофор', xlabel='Продолжительность сигнала светофора', marker='o')
    plt.savefig(pathToSave+'/vehicles_passed_mean.png', dpi=600)
    plt.show()
