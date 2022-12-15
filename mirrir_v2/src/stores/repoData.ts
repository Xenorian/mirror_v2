import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import type { List } from 'echarts'

const m_rooturl='http://10.181.247.163:8000'

// interface LanguageDetail{
//   value:  number;
//   name: string;
// }

// interface BasicData{
//   stars: number;
//   pulls: number;
//   issues: number;
//   open_pulls: number;
//   language: string;
//   language_detail: Array<LanguageDetail>
//   forks: number;
//   description: string;
//   contributor: number;
//   close_pulls: number;
// }

// interface Data{
//   basicData: BasicData
// }

export const repoDataStore = defineStore('repoData',{
  state: () =>({
    val: [],
    repos: [],
    repoList: []
  }),
  // persist: {
  //   //这里存储默认使用的是session
  //     enabled: true,
  //   },
  actions: {
    async addData() {
      let tmp_data={};

      for(let i=0;i<this.repos.length;i++){
        try{
          // basic data
          await axios
          .get(m_rooturl + "/get_basic",{
            params: {
              repo: this.repos[i].repo,
              user: this.repos[i].owner
            }
          })
          .then(response => {
            tmp_data.basicData = JSON.parse(response.data)
            turn_into_percentage(tmp_data.basicData.language_detail)
          })
  
          // commit activity
          await axios
          .get(m_rooturl + "/get_day_count",{
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'commit'
            }
          })
          .then(response => {
            tmp_data.commitActivity = JSON.parse(response.data)
          })

          // issue activity
          await axios
          .get(m_rooturl + "/get_day_count",{
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'issues'
            }
          })
          .then(response => {
            tmp_data.issueActivity = JSON.parse(response.data)
          })
          
          // pr activity
          await axios
          .get(m_rooturl + "/get_day_count",{
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'pulls'
            }
          })
          .then(response => {
            tmp_data.prActivity = JSON.parse(response.data)
          })

          // company data - commit
          await axios
          .get(m_rooturl + '/get_creator', {
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'commit'
            },
          })
          .then(response => {
            tmp_data.bubbledata = JSON.parse(response.data).result
          })

          // company data - issue
          await axios
          .get(m_rooturl + '/get_creator', {
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'issues'
            },
          })
          .then(response => {
            tmp_data.bubbledata_issue = JSON.parse(response.data).result
          })

          // company data - pr
          await axios
          .get(m_rooturl + '/get_creator', {
            params: {
              repo: this.repos[i].repo,
              owner: this.repos[i].owner,
              type: 'pulls'
            },
          })
          .then(response => {
            tmp_data.bubbledata_pr = JSON.parse(response.data).result
          })
  
          // user data
          await axios
          .get(m_rooturl + '/get_user' , {
            params: {
              owner: this.repos[i].owner,
              repo: this.repos[i].repo
            }
          })
          .then(response => {
            tmp_data.userData = JSON.parse(response.data).result
          })
  
          console.log(tmp_data)
          this.val[i] = (tmp_data)
          // let cpy = JSON.parse(JSON.stringify(tmp_data));
          // this.val.push(cpy)
        } catch (err){
          console.log(err)
        }
      }
    },
    
    async getRepoList() {
      await axios
      .get(m_rooturl + '/get_all')
      .then(response => {
        this.repoList = JSON.parse(response.data)
      })
    },

    addRepo(ownerName: String,repoName: String){
      for(let i=0;i<this.repos.length;i++){
        if(this.repos[i].repo===repoName&&
        this.repos[i].owner===ownerName){
          return;
        }
      }

      this.repos.push({
        repo: repoName,
        owner: ownerName
      })
    },

    clearData(){
      this.repos=[];
      this.val=[];
    }
  },
})

// deal with language_detail
function turn_into_percentage( language_detail ){
  // sum all
  let all_line = 0;
  for(let i=0;i<language_detail.length;i++){
    all_line+= language_detail[i].value;
  }

  // divide all
  for(let i=0;i<language_detail.length;i++){
    language_detail[i].value /=  all_line;
  }

}